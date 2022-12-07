# short_desc: auto name from configuration
class AutoName(dict):
        
    def get_path(self, cfg, path):
        output = cfg
        parts = path.split(".")
        for part in parts:
            output = output[part]
        return output
        
    def __call__(self, cfg):
        parts = dict()
        for name, path in self.items():
            parts[name] = self.get_path(cfg, path)
        return ','.join(f"{name}={value}" for (name, value) in parts.items())
