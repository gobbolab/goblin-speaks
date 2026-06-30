from src.config import Config


class SequencePlayer:

    def __init__(self, components: dict):
        self.components = components
        config = Config()
        self._sequences = config.get('sequences', {})

    @property
    def sequence_names(self):
        return list(self._sequences.keys())

    def play(self, sequence_name):
        sequence = self._get_sequence(sequence_name)

        print(f"Starting sequence '{sequence_name}'...")
        outputs = {}

        for i, step in enumerate(sequence):
            component_name = step.get('component')
            action_name = step.get('action')

            component = self._get_component(i, component_name)
            self._validate_action(i, component, component_name, action_name)

            raw_args = step.get('args', {})
            resolved_args = self._resolve_args(raw_args, outputs)

            print(f"  Step {i + 1}: {component_name}.{action_name}({resolved_args})")
            method = getattr(component, action_name)
            result = method(**resolved_args)

            output_name = step.get('output')
            if output_name:
                outputs[output_name] = result

        print(f"Sequence '{sequence_name}' finished.")

    def _get_sequence(self, sequence_name):
        if sequence_name not in self._sequences:
            raise ValueError(
                f"Unknown sequence '{sequence_name}'. "
                f"Available: {list(self._sequences.keys())}"
            )
        return self._sequences[sequence_name]

    def _get_component(self, step_index, component_name):
        if component_name not in self.components:
            raise ValueError(
                f"Sequence step {step_index + 1} references unknown component '{component_name}'. "
                f"Available: {list(self.components.keys())}"
            )
        return self.components[component_name]

    def _validate_action(self, step_index, component, component_name, action_name):
        if not hasattr(component, action_name):
            raise ValueError(
                f"Sequence step {step_index + 1}: component '{component_name}' "
                f"has no action '{action_name}'"
            )

    def _resolve_args(self, raw_args, outputs):
        resolved = {}
        for key, value in raw_args.items():
            resolved[key] = self._resolve_value(value, outputs)
        return resolved

    def _resolve_value(self, value, outputs):
        if isinstance(value, str) and value.startswith('$'):
            ref_name = value[1:]
            if ref_name not in outputs:
                raise ValueError(
                    f"Sequence references output '${ref_name}' "
                    f"but it has not been produced yet. "
                    f"Available: {list(outputs.keys())}"
                )
            return outputs[ref_name]
        if isinstance(value, list):
            return [self._resolve_value(v, outputs) for v in value]
        return value

    def shutdown(self):
        for name, component in self.components.items():
            if hasattr(component, 'shutdown'):
                print(f"Shutting down '{name}'...")
                component.shutdown()
