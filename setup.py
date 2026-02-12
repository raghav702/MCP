"""Setup script to configure the project."""
import os
import sys
from pathlib import Path


def create_env_file():
    """Create .env file from template."""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    if env_example.exists():
        # Copy template
        with open(env_example) as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env and add your API key!")
    else:
        print("❌ .env.example not found")


def create_directories():
    """Create necessary directories."""
    dirs = ["reports", "src"]
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    
    print("✅ Created project directories")


def check_python_version():
    """Check Python version."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def main():
    """Run setup."""
    print("\n🔧 Setting up Research Assistant Agent\n")
    
    if not check_python_version():
        return
    
    create_directories()
    create_env_file()
    
    print("\n" + "="*50)
    print("Setup complete! Next steps:")
    print("="*50)
    print("\n1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. Add your API key to .env file:")
    print("   OPENAI_API_KEY=your_key_here")
    print("\n3. Run the agent:")
    print("   python main.py")
    print("\n4. Or run tests:")
    print("   python test_agent.py")
    print()


if __name__ == "__main__":
    main()
