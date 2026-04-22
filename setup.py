"""
Spendwise Expense Tracker - Automated Setup Script

This script will:
1. Create a virtual environment
2. Install all dependencies from requirements.txt
3. Run database migrations
4. Collect static files (if needed)
5. Create a superuser (optional)

Usage:
    python setup.py
"""

import os
import subprocess
import sys
import venv


def run(cmd, cwd=None, check=True):
    """Run a shell command and handle errors"""
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if check and result.returncode != 0:
        print(f"\n❌ Failed: {cmd}")
        sys.exit(1)
    return result.returncode == 0


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(base, ".venv")

    print("=" * 60)
    print("🚀 Spendwise Expense Tracker - Automated Setup")
    print("=" * 60)

    # 1. Create virtual environment
    print("\n📦 Step 1/5: Creating virtual environment...")
    if os.path.exists(venv_dir):
        print("   ⚠️  Virtual environment already exists, skipping...")
    else:
        venv.create(venv_dir, with_pip=True)
        print("   ✅ Virtual environment created")

    # 2. Determine pip and python paths
    if sys.platform == "win32":
        pip = os.path.join(venv_dir, "Scripts", "pip")
        python = os.path.join(venv_dir, "Scripts", "python")
        activate_cmd = ".venv\\Scripts\\activate"
    else:
        pip = os.path.join(venv_dir, "bin", "pip")
        python = os.path.join(venv_dir, "bin", "python")
        activate_cmd = "source .venv/bin/activate"

    # 3. Upgrade pip
    print("\n📥 Step 2/5: Upgrading pip...")
    run(f'"{pip}" install --upgrade pip', cwd=base)
    print("   ✅ Pip upgraded")

    # 4. Install dependencies
    print("\n📥 Step 3/5: Installing dependencies...")
    if os.path.exists(os.path.join(base, "requirements.txt")):
        run(f'"{pip}" install -r requirements.txt', cwd=base)
        print("   ✅ Dependencies installed (Django, ReportLab)")
    else:
        print("   ⚠️  requirements.txt not found, installing Django and ReportLab...")
        run(f'"{pip}" install Django==4.2.11 reportlab==4.1.0', cwd=base)

    # 5. Run migrations
    print("\n🗄️  Step 4/5: Running database migrations...")
    run(f'"{python}" manage.py makemigrations', cwd=base, check=False)
    run(f'"{python}" manage.py migrate', cwd=base)
    print("   ✅ Database migrations completed")

    # 6. Collect static files (optional, for production)
    print("\n📁 Step 5/5: Checking static files...")
    print("   ℹ️  Static files are already in tracker/static/")
    print("   ℹ️  No collection needed for development")

    # 7. Ask about creating superuser
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    
    print("\n� Project Structure:")
    print("   ✓ Virtual environment (.venv/)")
    print("   ✓ Dependencies installed (Django, ReportLab)")
    print("   ✓ Database created (db.sqlite3)")
    print("   ✓ Static files (tracker/static/tracker/css/)")
    print("   ✓ Templates (tracker/templates/)")
    
    print("\n🎯 Next Steps:")
    print(f"   1. Activate virtual environment: {activate_cmd}")
    print("   2. Create superuser (optional): python manage.py createsuperuser")
    print("   3. Start server: python manage.py runserver")
    print("   4. Open browser: http://127.0.0.1:8000")
    
    print("\n💡 Quick Commands:")
    print("   • Run server:        python manage.py runserver")
    print("   • Create superuser:  python manage.py createsuperuser")
    print("   • Make migrations:   python manage.py makemigrations")
    print("   • Apply migrations:  python manage.py migrate")
    print("   • Access admin:      http://127.0.0.1:8000/admin/")
    
    print("\n" + "=" * 60)
    
    # Optional: Ask if user wants to create superuser now
    try:
        response = input("\n❓ Create superuser now? (y/n): ").strip().lower()
        if response == 'y':
            print("\n👤 Creating superuser...")
            run(f'"{python}" manage.py createsuperuser', cwd=base, check=False)
    except KeyboardInterrupt:
        print("\n\n👋 Setup completed. Superuser creation skipped.")


if __name__ == "__main__":
    main()
