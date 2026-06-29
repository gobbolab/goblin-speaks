import inspect


class PluginGenerator:

    @classmethod
    def generate_skeleton(cls, base_class, plugin_name):
        class_name = cls._snake_to_pascal(plugin_name)
        base_name = base_class.__name__

        lines = []
        lines.append(f"class {class_name}({base_name}):")

        # Constructor — call super().__init__ if the base class defines one
        lines.append("    def __init__(self, config_prefix=None):")
        if '__init__' in base_class.__dict__:
            lines.append("        super().__init__(config_prefix)")
        lines.append(f'        print("TODO: initialize {class_name}")')
        lines.append("")

        # Generate stubs for each abstract method
        for method_name in sorted(base_class.__abstractmethods__):
            method = getattr(base_class, method_name)
            sig = inspect.signature(method)
            params = []
            for pname, param in sig.parameters.items():
                if pname == 'self':
                    params.append('self')
                elif param.annotation is not inspect.Parameter.empty:
                    hint = param.annotation.__name__ if isinstance(param.annotation, type) else str(param.annotation)
                    params.append(f"{pname}: {hint}")
                elif param.default is not inspect.Parameter.empty:
                    params.append(f"{pname}={param.default!r}")
                else:
                    params.append(pname)

            lines.append(f"    def {method_name}({', '.join(params)}):")
            lines.append(f'        print("TODO: implement {method_name}")')
            lines.append("")

        return "\n".join(lines) + "\n"

    @staticmethod
    def _snake_to_pascal(name):
        return ''.join(word.capitalize() for word in name.split('_'))
