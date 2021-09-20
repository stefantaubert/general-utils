

def disable_matplot_logger():
  disable_matplot_font_logger()
  disable_matplot_colorbar_logger()


def disable_numba_logger():
  disable_numba_core_logger()


def disable_numba_core_logger():
  """
  Disables:
    DEBUG:numba.core.ssa:on stmt: $92load_attr.32 = getattr(value=y, attr=shape)
    DEBUG:numba.core.ssa:on stmt: $const94.33 = const(int, 1)
    DEBUG:numba.core.ssa:on stmt: $96binary_subscr.34 = static_getitem(value=$92load_attr.32, index=1, index_var=$const94.33, fn=<built-in function getitem>)
    DEBUG:numba.core.ssa:on stmt: n_channels = $96binary_subscr.34
    DEBUG:numba.core.ssa:on stmt: $100load_global.35 = global(range: <class 'range'>)
    DEBUG:numba.core.ssa:on stmt: $104call_function.37 = call $100load_global.35(n_out, func=$100load_global.35, args=[Var(n_out, interpn.py:24)], kws=(), vararg=None)
    DEBUG:numba.core.ssa:on stmt: $106get_iter.38 = getiter(value=$104call_function.37)
    DEBUG:numba.core.ssa:on stmt: $phi108.0 = $106get_iter.38
    DEBUG:numba.core.ssa:on stmt: jump 108
    DEBUG:numba.core.byteflow:block_infos State(pc_initial=446 nstack_initial=1):
    AdaptBlockInfo(insts=((446, {'res': '$time_register446.1'}), (448, {'res': '$time_increment448.2'}), (450, {'lhs': '$time_register446.1', 'rhs': '$time_increment448.2', 'res': '$450inplace_add.3'}), (452, {'value': '$450inplace_add.3'}),
    (454, {})), outgoing_phis={}, blockstack=(), active_try_block=None, outgoing_edgepushed={108: ('$phi446.0',)})
    DEBUG:numba.core.byteflow:block_infos State(pc_initial=456 nstack_initial=0):
    AdaptBlockInfo(insts=((456, {'res': '$const456.0'}), (458, {'retval': '$const456.0', 'castval': '$458return_value.1'})), outgoing_phis={}, blockstack=(), active_try_block=None, outgoing_edgepushed={})
    DEBUG:numba.core.interpreter:label 0:
        x = arg(0, name=x)                       ['x']
        y = arg(1, name=y)                       ['y']
        sample_ratio = arg(2, name=sample_ratio) ['sample_ratio']
    ...
  """
  logging.getLogger('numba.core').disabled = True


def disable_matplot_font_logger():
  '''
  Disables:
    DEBUG:matplotlib.font_manager:findfont: score(<Font 'Noto Sans Oriya UI' (NotoSansOriyaUI-Bold.ttf) normal normal 700 normal>) = 10.335
    DEBUG:matplotlib.font_manager:findfont: score(<Font 'Noto Serif Khmer' (NotoSerifKhmer-Regular.ttf) normal normal 400 normal>) = 10.05
    DEBUG:matplotlib.font_manager:findfont: score(<Font 'Samyak Gujarati' (Samyak-Gujarati.ttf) normal normal 500 normal>) = 10.14
    ...
  '''
  logging.getLogger('matplotlib.font_manager').disabled = True


def disable_matplot_colorbar_logger():
  '''
  Disables:
    DEBUG:matplotlib.colorbar:locator: <matplotlib.colorbar._ColorbarAutoLocator object at 0x7f78f08e6370>
    DEBUG:matplotlib.colorbar:Using auto colorbar locator <matplotlib.colorbar._ColorbarAutoLocator object at 0x7f78f08e6370> on colorbar
    DEBUG:matplotlib.colorbar:Setting pcolormesh
  '''
  logging.getLogger('matplotlib.colorbar').disabled = True
