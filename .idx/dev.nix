{ pkgs, ... }: {
  channel = "stable-23.11";
  packages = [ pkgs.python312 pkgs.python312Packages.pip pkgs.nodejs_20 pkgs.redis ];
  env = { PYTHONPATH = "./backend"; };
  idx = {
    extensions = [ "ms-python.python" "ms-python.black-formatter" "esbenp.prettier-vscode" "bradlc.vscode-tailwindcss" ];
    previews = {
      enable = true;
      previews = {
        backend = {
          command = [ "bash" "-c" "cd backend && pip install -r requirements.txt -q && uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload" ];
          manager = "web"; port = 8000;
        };
        frontend = {
          command = [ "bash" "-c" "cd frontend && npm install --legacy-peer-deps && npm run dev -- --port $PORT --host" ];
          manager = "web"; port = 3000;
        };
      };
    };
    workspace = {
      onCreate = {
        install-backend = "cd backend && pip install -r requirements.txt";
        install-frontend = "cd frontend && npm install --legacy-peer-deps";
      };
      onStart = { start-redis = "redis-server --daemonize yes"; };
    };
  };
}
