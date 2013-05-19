from collections import OrderedDict

def group_review_criteria(reviews):
	data_by_criterias = OrderedDict()
	for review in reviews:
		criterias = review.criteria_set.all()
		for crit in criterias:
			if crit.attribute not in data_by_criterias:
				data_by_criterias[crit.attribute] = [[], []]
			data_by_criterias[crit.attribute][0].append(crit.value)
			data_by_criterias[crit.attribute][1].append(crit.comment)
		ev = review.evaluation
		if ev.attribute not in data_by_criterias:
			data_by_criterias[ev.attribute] = [[], []]
		data_by_criterias[ev.attribute][0].append(ev.value)
		data_by_criterias[ev.attribute][1].append(ev.comment)

	return data_by_criterias
