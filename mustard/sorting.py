# Copyright (C) 2012 Codethink Limited


from itertools import groupby


def comparator(sort_key):
    def compare_elements(pair1, pair2):
        def split_by_numbers(s):
            return [''.join(v) for _, v in groupby(s, lambda c: c.isdigit())]

        s1 = getattr(pair1[1], sort_key) if pair1 and pair1[1] else ''
        s2 = getattr(pair2[1], sort_key) if pair2 and pair2[1] else ''

        s1s = split_by_numbers(s1)
        s2s = split_by_numbers(s2)

        s1s.append('')
        s2s.append('')

        for left, right in zip(s1s, s2s):
            leftdigit = left.isdigit()
            rightdigit = right.isdigit()
            if leftdigit and rightdigit:
                cmpres = cmp(int(left), int(right))
                if cmpres != 0:
                    return cmpres
            elif leftdigit:
                return 1 if right == "" else -1
            elif rightdigit:
                return -1 if left == "" else 1
            cmpres = cmp(left, right)
            if cmpres != 0:
                return cmpres
        return 0

    return compare_elements


def sort_elements(elements, args):
    real_elements = [e for p, e in elements if e is not None]
    if real_elements:
        default_sort_by = real_elements[0].tree.project.sort_by
    else:
        default_sort_by = None
    sort_by = args.get('sort_by', None)
    if sort_by == 'DEFAULT':
        sort_by = default_sort_by
    reverse = args.get('reverse', False)
    if sort_by:
        return sorted(elements, cmp=comparator(sort_by), reverse=reverse)
    else:
        return elements
