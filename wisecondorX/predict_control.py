# WisecondorX

'''
Control function that executes following
normalization strategies:
- coverage normalization
- between-sample normalization
- within-sample normalization
'''

def normalize(args, sample, ref_file, ref_gender):

	if ref_gender == 'A':
		ap = ''
		ct = 0
	else:
		ap = '.{}'.format(ref_gender)
		ct = ref_file['masked_bins_per_chr_cum'][21]

	from predict_tools import coverage_normalize_and_mask, project_pc, get_optimal_cutoff, get_weights, normalize_repeat
	sample = coverage_normalize_and_mask(sample, ref_file, ap)
	sample = project_pc(sample, ref_file, ap)
	results_w = get_weights(ref_file, ap)
	optimal_cutoff = get_optimal_cutoff(ref_file, args.maskrepeats, ap)
	results_z, results_r, ref_sizes = normalize_repeat(sample, ref_file, optimal_cutoff, 5, ap)

	return results_r[ct:], results_z[ct:], results_w[ct:], ref_sizes[ct:]


'''
Function processes a result (e.g. results_r)
to an easy-to-interpret format. Bins without
information are set to 0.
'''

def get_post_processed_result(args, result, ref_sizes, rem_input):
	infinite_mask = (ref_sizes < args.minrefbins)
	result[infinite_mask] = 0
	from predict_tools import inflate_results
	inflated_results = inflate_results(result, rem_input)

	final_results = []
	for chr in range(len(rem_input['bins_per_chr'])):
		chr_data = inflated_results[sum(rem_input['bins_per_chr'][:chr]):sum(rem_input['bins_per_chr'][:chr + 1])]
		final_results.append(chr_data)

	final_results = [x.tolist() for x in final_results]

	return final_results