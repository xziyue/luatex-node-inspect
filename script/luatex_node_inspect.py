import copy
import re
import os
import json

__node_common_field = [
    'id', 'prev', 'next', 'subtype'
]

__node_id = {
    0: 'hlist', 1: 'vlist', 2: 'rule', 3: 'ins', 4: 'mark', 5: 'adjust', 6: 'boundary', 7: 'disc', 8: 'whatsit',
    9: 'local_par', 10: 'dir', 11: 'math', 12: 'glue', 13: 'kern', 14: 'penalty', 15: 'unset', 16: 'style',
    17: 'choice', 18: 'noad', 19: 'radical', 20: 'fraction', 21: 'accent', 22: 'fence', 23: 'math_char', 24: 'sub_box',
    25: 'sub_mlist', 26: 'math_text_char', 27: 'delim', 28: 'margin_kern', 29: 'glyph', 30: 'align_record',
    31: 'pseudo_file', 32: 'pseudo_line', 33: 'page_insert', 34: 'split_insert', 35: 'expr_stack', 36: 'nested_list',
    37: 'span', 38: 'attribute', 39: 'glue_spec', 40: 'attribute_list', 41: 'temp', 42: 'align_stack',
    43: 'movement_stack', 44: 'if_stack', 45: 'unhyphenated', 46: 'hyphenated', 47: 'delta', 48: 'passive', 49: 'shape'
}

_hlist_field = [
    'attr', 'width', 'height', 'depth', 'shift', 'glue_order', 'glue_set', 'glue_sign',
    'head', 'list', 'dir'
]

hlist_subtype = {
    0: 'unknown', 1: 'line', 2: 'box', 3: 'indent', 4: 'alignment', 5: 'cell', 6: 'equation', 7: 'equationnumber',
    8: 'math', 9: 'mathchar', 10: 'hextensible', 11: 'vextensible', 12: 'hdelimiter', 13: 'vdelimiter',
    14: 'overdelimiter', 15: 'underdelimiter', 16: 'numerator', 17: 'denominator', 18: 'limits', 19: 'fraction',
    20: 'nucleus', 21: 'sup', 22: 'sub', 23: 'degree', 24: 'scripts', 25: 'over', 26: 'under', 27: 'accent',
    28: 'radical'
}

hlist_glue_sign = {
    0: 'normal',
    1: 'stretching',
    2: 'shrinking'
}

_vlist_field = copy.copy(_hlist_field)

vlist_subtype = {
    0: 'unknown',
    4: 'alignment',
    5: 'cell'
}

_rule_field = [
    'attr', 'width', 'height', 'depth',
    'left', 'right', 'dir', 'index', 'transform'
]

rule_subtype = {
    0: 'normal', 1: 'box', 2: 'image', 3: 'empty', 4: 'user', 5: 'over', 6: 'under', 7: 'fraction', 8: 'radical',
    9: 'outline'
}

_ins_field = [
    'attr', 'cost', 'height', 'depth', 'head', 'list'
]

_mark_field = [
    'attr', 'class', 'mark'
]

_adjust_field = [
    'attr', 'head', 'list'
]

adjust_subtype = {
    0: 'normal',
    1: 'pre'
}

_disc_field = [
    'attr', 'pre', 'post', 'replace', 'penalty'
]

disc_subtype = {
    0: 'discretionary', 1: 'explicit', 2: 'automatic', 3: 'regular', 4: 'first', 5: 'second'
}

_math_field = [
    'attr', 'surround'
]

math_subtype = {
    0: 'beginmath', 1: 'endmath'
}

_glue_field = [
    'width', 'stretch', 'stretch_over', 'shrink', 'shrink_over', 'attr', 'leader'
]

glue_subtype = {
    0: 'userskip', 1: 'lineskip', 2: 'baselineskip', 3: 'parskip', 4: 'abovedisplayskip', 5: 'belowdisplayskip',
    6: 'abovedisplayshortskip', 7: 'belowdisplayshortskip', 8: 'leftskip', 9: 'rightskip', 10: 'topskip',
    11: 'splittopskip', 12: 'tabskip', 13: 'spaceskip', 14: 'xspaceskip', 15: 'parfillskip', 16: 'mathskip',
    17: 'thinmuskip', 18: 'medmuskip', 19: 'thickmuskip', 98: 'conditionalmathskip', 99: 'muglue', 100: 'leaders',
    101: 'cleaders', 102: 'xleaders', 103: 'gleaders'
}

_kern_field = [
    'attr', 'kern'
]

kern_subtype = {
    0: 'footkern', 1: 'userkern', 2: 'accentkern', 3: 'italiccorrection'
}

_penalty_field = [
    'attr', 'penalty'
]

penalty_subtype = {
    0: 'userpenalty', 1: 'linebreakpenalty', 2: 'linepenalty', 3: 'wordpenalty', 4: 'finalpenalty', 5: 'noadpenalty',
    6: 'beforedisplaypenalty', 7: 'afterdisplaypenalty', 8: 'equationnumberpenalty'
}

_glyph_field = [
    'attr', 'char', 'font', 'lang', 'left', 'right', 'uchyph',
    'components', 'xoffset', 'yoffset', 'width', 'height', 'depth',
    'expansion_factor', 'data'
]

glyph_subtype = {
    0: '', 1: 'character', 2: 'ligature', 3: 'ligature+character', 4: 'ghost', 5: 'ghost+character',
    6: 'ghost+ligature', 7: 'ghost+ligature+character', 8: 'left', 9: 'left+character', 10: 'left+ligature',
    11: 'left+ligature+character', 12: 'left+ghost', 13: 'left+ghost+character', 14: 'left+ghost+ligature',
    15: 'left+ghost+ligature+character', 16: 'right', 17: 'right+character', 18: 'right+ligature',
    19: 'right+ligature+character', 20: 'right+ghost', 21: 'right+ghost+character', 22: 'right+ghost+ligature',
    23: 'right+ghost+ligature+character', 24: 'right+left', 25: 'right+left+character', 26: 'right+left+ligature',
    27: 'right+left+ligature+character', 28: 'right+left+ghost', 29: 'right+left+ghost+character',
    30: 'right+left+ghost+ligature', 31: 'right+left+ghost+ligature+character'
}

_boundary_field = [
    'attr', 'value'
]

_local_par_field = [
    'attr', 'pen_inter', 'pen_broken', 'dir', 'box_left', 'box_left_width',
    'box_right', 'box_right_width'
]

_dir_field = [
    'attr', 'dir', 'level'
]

_marginkern_field = [
    'attr', 'width', 'glyph'
]

marginkern_subtype = {
    0: 'left', 1: 'right'
}

_math_char_field = [
    'attr', 'char', 'fam'
]

_math_text_char_field = copy.copy(_math_char_field)

_sub_box_field = [
    'attr', 'head', 'list'
]

_sub_mlist_field = copy.copy(_sub_box_field)

_delim_field = [
    'attr', 'small_char', 'small_fam', 'large_char', 'large_fam'
]

__math_options = {8: 'set/internal', 9: 'internal', 10: 'axis', 12: 'no axis', 24: 'exact', 25: 'left', 26: 'middle',
                  28: 'right', 41: 'no sub script', 42: 'no super script', 43: 'no script'}

_noad_field = [
    'attr', 'nucleus', 'sub', 'sup', 'options'
]

noad_subtype = {
    0: 'ord', 1: 'opdisplaylimits', 2: 'oplimits', 3: 'opnolimits', 4: 'bin', 5: 'rel', 6: 'open', 7: 'close',
    8: 'punct', 9: 'inner', 10: 'under', 11: 'over', 12: 'vcenter'
}

_accent_field = [
    'nucleus', 'sub', 'sup', 'accent', 'bot_accent', 'fraction'
]

accent_subtype = {
    0: 'bothflexible', 1: 'fixedtop', 2: 'fixedbottom', 3: 'fixedboth'
}

_style_field = [
    'style'
]

_choice_field = [
    'attr', 'display', 'text', 'script', 'scriptscript'
]

_radical_field = [
    'attr', 'nucleus', 'sub', 'sup', 'left', 'degree', 'width', 'options'
]

radical_subtype = {
    0: 'radical', 1: 'uradical', 2: 'uroot', 3: 'uunderdelimiter', 4: 'uoverdelimiter', 5: 'udelimiterunder',
    6: 'udelimiterover'
}

_fraction_field = [
    'attr', 'width', 'num', 'denom', 'left', 'right', 'middle', 'options'
]

_fence_field = [
    'attr', 'delim', 'italic', 'height', 'depth', 'options', 'class'
]

__whatsit_id = {'0': 'open', '1': 'write', '2': 'close', '3': 'special', '6': 'save_pos', '7': 'late_lua',
                '8': 'user_defined', '16': 'pdf_literal', '17': 'pdf_refobj', '18': 'pdf_annot', '19': 'pdf_start_link',
                '20': 'pdf_end_link', '21': 'pdf_dest', '22': 'pdf_action', '23': 'pdf_thread',
                '24': 'pdf_start_thread', '25': 'pdf_end_thread', '26': 'pdf_thread_data', '27': 'pdf_link_data',
                '28': 'pdf_colorstack', '29': 'pdf_setmatrix', '30': 'pdf_save', '31': 'pdf_restore'}

_whatsit_open_field = [
    'attr', 'stream', 'name', 'ext', 'area'
]

_whatsit_write_field = [
    'attr', 'stream', 'data'
]

_whatsit_close_field = [
    'attr', 'stream'
]

_whatsit_user_defined_field = [
    'attr', 'user_id', 'type', 'value'
]

whatsit_user_defined_type =  {
    97: 'attribute list',
    100: 'Lua number',
    108: 'Lua value',
    110: 'node list',
    115: 'Lua string',
    116: 'Lua token list'
}

_whatsit_save_pos_field = [
    'attr'
]

_whatsit_late_lua_field = [
    'attr', 'data', 'token', 'name'
]

_whatsit_special_field = [
    'attr', 'data'
]

_whatsit_pdf_literal_field = [
    'attr', 'mode', 'data', 'token'
]

whatsit_pdf_literal_mode = {
    0: 'origin',
    1: 'page',
    2: 'direct',
    3: 'raw',
    4: 'text'
}

_whatsit_pdf_refobj_field = [
    'attr', 'objnum'
]

_whatsit_pdf_annot_field = [
    'attr', 'width', 'height', 'depth', 'objnum', 'data'
]

_whatsit_pdf_start_link_field = [
    'attr', 'width', 'height', 'depth', 'objnum', 'link_attr', 'action'
]

_whatsit_pdf_end_link_field = [
    'attr'
]

_whatsit_pdf_dest_field = [
    'attr', 'width', 'height', 'depth', 'named_id', 'dest_id', 'dest_type', 'xyz_zoom', 'objnum'
]

_whatsit_pdf_action_field = [
    'action_type', 'action_id', 'named_id', 'file', 'new_window', 'data'
]

whatsit_pdf_action_action_type = {
    0: 'page',
    1: 'goto',
    2: 'thread',
    3: 'user'
}

whatsit_pdf_action_new_window = {
    0: 'notset',
    1: 'new',
    2: 'nonew'
}

_whatsit_pdf_thread_field = [
    'attr', 'width', 'height', 'depth', 'named_id', 'thread_id', 'thread_attr'
]

_whatsit_pdf_start_thread_field = [
    'attr', 'width', 'height', 'depth', 'named_id', 'thread_id', 'thread_attr'
]

_whatsit_pdf_end_thread_field = [
    'attr'
]

_whatsit_pdf_colorstack_field = [
    'attr', 'stack', 'command', 'data'
]

_whatsit_pdf_setmatrix_field = [
    'attr', 'data'
]

_whatsit_pdf_save_field = [
    'attr'
]

_whatsit_pdf_restore_field = [
    'attr'
]

__luatex_variables = []
__global_keys = list(globals().keys())
for key in __global_keys:
    val = globals()[key]
    if isinstance(val, (dict, list)):
        start_match = re.match('(_+).*', key)
        if start_match is None or len(start_match.group(1)) < 2:
            __luatex_variables.append(key)

# construct output json
__defined_nodes = []
for key in __luatex_variables:
    match = re.match('_(.*?)_field', key)
    if match is not None:
        old_length = len(globals()[key])
        globals()[key] = __node_common_field + globals()[key]
        # integrity check
        # print(key)
        # print(len(set(globals()[key])), old_length + len(__node_common_field))
        assert isinstance(globals()[key], list)
        assert len(set(globals()[key])) == old_length + len(__node_common_field)
        __defined_nodes.append(match.group(1))

print(__defined_nodes)

__output_dict = {}
__output_dict['_node_id'] = __node_id
__output_dict['_math_options'] = __math_options
__output_dict['_whatsit_id'] = __whatsit_id
for node in __defined_nodes:
    __output_dict[node] = dict()
    __output_dict[node]['_field'] = globals()['_' + node + '_field']
    for var_name in __luatex_variables:
        if var_name.startswith(node):
            key_name = var_name[len(node) + 1:]
            __output_dict[node][key_name] = globals()[var_name]

with open(os.path.join('..', 'luatex-node.json'), 'w') as outfile:
    json.dump(__output_dict, outfile, indent=2)
