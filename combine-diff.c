	struct combine_diff_path *p;
	int i;
		struct combine_diff_path *list = NULL, **tail = &list;
			p->len = len;
		return list;
	for (p = curr; p; p = p->next) {
		int found = 0;
		if (!p->len)
		for (i = 0; i < q->nr; i++) {
			const char *path;
			int len;
			if (diff_unmodified_pair(q->queue[i]))
				continue;
			path = q->queue[i]->two->path;
			len = strlen(path);
			if (len == p->len && !memcmp(path, p->path, len)) {
				found = 1;
				hashcpy(p->parent[n].sha1, q->queue[i]->one->sha1);
				p->parent[n].mode = q->queue[i]->one->mode;
				p->parent[n].status = q->queue[i]->status;
				break;
			}
		if (!found)
			p->len = 0;
	struct lline *next;
	struct lline *lost_head, **lost_tail;
	struct lline *next_lost;
	/* Check to see if we can squash things */
	if (sline->lost_head) {
		lline = sline->next_lost;
		while (lline) {
			if (lline->len == len &&
			    !memcmp(lline->line, line, len)) {
				lline->parent_map |= this_mask;
				sline->next_lost = lline->next;
				return;
			}
			lline = lline->next;
		}
	}

	*sline->lost_tail = lline;
	sline->lost_tail = &lline->next;
	sline->next_lost = NULL;
		state->lost_bucket->next_lost = state->lost_bucket->lost_head;
			 const char *path)
	xpp.flags = 0;
		ll = sline[lno].lost_head;
	return ((sline->flag & all_mask) || sline->lost_head);
		while (j < i)
			sline[j++].flag |= mark | no_pre_delete;
			struct lline *ll = sline[j].lost_head;
static void dump_sline(struct sline *sline, unsigned long cnt, int num_parent,
		fputs(c_frag, stdout);
			ll = (sl->flag & no_pre_delete) ? NULL : sl->lost_head;
				fputs(c_old, stdout);
		struct lline *ll = sline->lost_head;
			 "", elem->path, c_meta, c_reset);
	printf("%sindex ", c_meta);
			printf("%snew file mode %06o",
			       c_meta, elem->mode);
				printf("%sdeleted file ", c_meta);
				 c_meta, c_reset);
				 c_meta, c_reset);
				 c_meta, c_reset);
				 c_meta, c_reset);
				     mode_differs, 0);
	for (lno = 0; lno <= cnt + 1; lno++) {
		sline[lno].lost_tail = &sline[lno].lost_head;
		sline[lno].flag = 0;
	}
				     textconv, elem->path);
				     mode_differs, 1);
		dump_sline(sline, cnt, num_parent,
		if (sline[lno].lost_head) {
			struct lline *ll = sline[lno].lost_head;
#define COLONS "::::::::::::::::::::::::::::::::"

	int i, offset;
	const char *prefix;
	int line_termination, inter_name_termination;
		offset = strlen(COLONS) - num_parent;
		if (offset < 0)
			offset = 0;
		prefix = COLONS + offset;
		for (i = 0; i < num_parent; i++) {
			printf("%s%06o", prefix, p->parent[i].mode);
			prefix = " ";
		}
		printf("%s%06o", prefix, p->mode);
	if (!p->len)
		return;
	for (i = 0, p = paths; p; p = p->next) {
		if (!p->len)
			continue;
	}
			if (rev->verbose_header && opt->output_format)
				putchar(opt->line_termination);
	/* find out surviving paths */
	for (num_paths = 0, p = paths; p; p = p->next) {
		if (p->len)
			num_paths++;
			for (p = paths; p; p = p->next) {
				if (p->len)
					show_raw_diff(p, num_parent, rev);
			}
				putchar(opt->line_termination);
			for (p = paths; p; p = p->next) {
				if (p->len)
					show_patch_diff(p, num_parent, dense,
							0, rev);
			}
	struct commit_list *parent = commit->parents;