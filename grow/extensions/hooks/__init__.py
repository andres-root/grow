"""Extension hooks."""

from . import dev_file_change_hook
from . import dev_handler_hook
from . import post_render_hook
from . import preprocess_hook

# pylint: disable=invalid-name
DevFileChangeHook = dev_file_change_hook.DevFileChangeHook
DevHandlerHook = dev_handler_hook.DevHandlerHook
PostRenderHook = post_render_hook.PostRenderHook
PreprocessHook = preprocess_hook.PreprocessHook

HOOKS = (
    dev_file_change_hook.DevFileChangeHook,
    dev_handler_hook.DevHandlerHook,
    post_render_hook.PostRenderHook,
    preprocess_hook.PreprocessHook,
)
