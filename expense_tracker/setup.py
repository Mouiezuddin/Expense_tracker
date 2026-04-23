import os
import subprocess
import sys
import venv


def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"\n❌ Failed: {cmd}")
        sys.exit(1)


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(base, ".venv")

    # 1. Create virtual environment
    print("\n📦 Creating virtual environment...")
    venv.create(venv_dir, with_pip=True)

    # 2. Determine pip and python paths
    if sys.platform == "win32":
        pip = os.path.join(venv_dir, "Scripts", "pip")
        python = os.path.join(venv_dir, "Scripts", "python")
    else:
        pip = os.path.join(venv_dir, "bin", "pip")
        python = os.path.join(venv_dir, "bin", "python")

    # 3. Install dependencies
    print("\n📥 Installing dependencies...")
    run(f'"{pip}" install -r requirements.txt', cwd=base)

    # 4. Run migrations
    print("\n🗄️  Running migrations...")
    run(f'"{python}" manage.py migrate', cwd=base)

    # 5. Done
    print("\n✅ Setup complete!")
    print("\n👉 To start the server:")
    if sys.platform == "win32":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("   python manage.py runserver")


if __name__ == "__main__":
    main()
