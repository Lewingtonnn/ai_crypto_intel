from app.config_loader import load_config

cfg=load_config()
print(cfg.project['name'])
print(cfg.embedding['model_name'])
