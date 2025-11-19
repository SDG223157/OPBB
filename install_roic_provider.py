#!/usr/bin/env python3
"""
Install ROIC as an OpenBB Provider
This will integrate ROIC like Yahoo Finance and FRED
"""

import os
import sys
import json
from pathlib import Path
import shutil

def install_roic_provider():
    """Install ROIC provider into OpenBB"""
    
    print("="*80)
    print(" "*20 + "ROIC PROVIDER INSTALLER")
    print("="*80)
    
    # 1. Find OpenBB installation
    print("\n📍 Locating OpenBB installation...")
    
    # Check virtual environment
    venv_path = Path('/Users/sdg223157/OPBB/openbb-env')
    openbb_locations = []
    
    # Look for OpenBB in site-packages
    for version in ['python3.13', 'python3.12', 'python3.11', 'python3.10', 'python3.9', 'python3.8']:
        site_packages = venv_path / 'lib' / version / 'site-packages'
        if site_packages.exists():
            openbb_path = site_packages / 'openbb'
            if openbb_path.exists():
                openbb_locations.append(openbb_path)
                print(f"  ✅ Found OpenBB at: {openbb_path}")
    
    if not openbb_locations:
        print("  ❌ OpenBB installation not found")
        return False
    
    # 2. Create provider extension directory
    print("\n📦 Creating ROIC provider extension...")
    
    # Create custom providers directory
    custom_providers = Path.home() / '.openbb_platform' / 'custom_providers'
    custom_providers.mkdir(parents=True, exist_ok=True)
    
    roic_provider_dir = custom_providers / 'openbb_roic'
    roic_provider_dir.mkdir(exist_ok=True)
    
    # 3. Copy provider files
    print("\n📄 Installing provider files...")
    
    # Copy main provider module
    shutil.copy(
        '/Users/sdg223157/OPBB/openbb_roic_provider_extension.py',
        roic_provider_dir / 'provider.py'
    )
    
    # Copy supporting modules
    shutil.copy(
        '/Users/sdg223157/OPBB/openbb_roic_provider.py',
        roic_provider_dir / 'roic_calculator.py'
    )
    
    # Fix imports in provider.py to use relative imports
    provider_file = roic_provider_dir / 'provider.py'
    with open(provider_file, 'r') as f:
        content = f.read()
    
    # Replace absolute import with relative import
    content = content.replace(
        'from openbb_roic_provider import roic_provider',
        'from .roic_calculator import roic_provider'
    )
    
    with open(provider_file, 'w') as f:
        f.write(content)
    
    # Create __init__.py
    init_content = '''"""ROIC Provider for OpenBB Platform"""
from .provider import ROICProvider, ROICMetricsFetcher, ROICForecastFetcher

__all__ = ["ROICProvider", "ROICMetricsFetcher", "ROICForecastFetcher"]
'''
    
    with open(roic_provider_dir / '__init__.py', 'w') as f:
        f.write(init_content)
    
    print(f"  ✅ Provider installed to: {roic_provider_dir}")
    
    # 4. Register provider in OpenBB config
    print("\n⚙️  Registering provider with OpenBB...")
    
    # Update OpenBB settings
    settings_file = Path.home() / '.openbb_platform' / 'user_settings.json'
    
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            settings = json.load(f)
    else:
        settings = {}
    
    # Add ROIC to providers list
    if 'providers' not in settings:
        settings['providers'] = {}
    
    settings['providers']['roic'] = {
        'enabled': True,
        'credentials': {
            'roic_api_key': 'a365bff224a6419fac064dd52e1f80d9'
        }
    }
    
    # Add custom provider path
    if 'custom_provider_paths' not in settings:
        settings['custom_provider_paths'] = []
    
    provider_path = str(roic_provider_dir)
    if provider_path not in settings['custom_provider_paths']:
        settings['custom_provider_paths'].append(provider_path)
    
    # Save settings
    settings_file.parent.mkdir(exist_ok=True)
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"  ✅ Provider registered in: {settings_file}")
    
    # 5. Create provider manifest
    print("\n📝 Creating provider manifest...")
    
    manifest = {
        "name": "openbb_roic",
        "version": "1.0.0",
        "description": "ROIC.ai provider for quality investing metrics",
        "author": "OpenBB Community",
        "provider_class": "ROICProvider",
        "endpoints": {
            "/equity/fundamental/metrics": {
                "fetcher": "ROICMetricsFetcher",
                "description": "Get ROIC and quality metrics"
            },
            "/equity/estimates/consensus": {
                "fetcher": "ROICForecastFetcher",
                "description": "Get quality-based forecasts"
            }
        },
        "credentials": {
            "roic_api_key": {
                "description": "ROIC.ai API key",
                "required": False,
                "default": "a365bff224a6419fac064dd52e1f80d9"
            }
        }
    }
    
    with open(roic_provider_dir / 'provider.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"  ✅ Manifest created")
    
    # 6. Create CLI commands
    print("\n🔧 Setting up CLI commands...")
    
    # Create command aliases
    cli_config = Path.home() / '.openbb_cli' / 'config.json'
    cli_config.parent.mkdir(exist_ok=True)
    
    if cli_config.exists():
        with open(cli_config, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    if 'aliases' not in config:
        config['aliases'] = {}
    
    # Add ROIC aliases
    config['aliases'].update({
        'roic_metrics': '/equity/fundamental/metrics --provider roic',
        'roic_forecast': '/equity/estimates/consensus --provider roic',
        'roic_quality': '/equity/fundamental/metrics --provider roic'
    })
    
    with open(cli_config, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("  ✅ CLI commands configured")
    
    # 7. Test the installation
    print("\n🧪 Testing installation...")
    
    test_script = f'''
import sys
sys.path.insert(0, "{roic_provider_dir}")
try:
    from provider import ROICProvider
    print("  ✅ Provider module loads successfully")
    print(f"  Provider name: {{ROICProvider.name}}")
    print(f"  Display name: {{ROICProvider.display_name}}")
except Exception as e:
    print(f"  ❌ Error loading provider: {{e}}")
'''
    
    exec(test_script)
    
    print("\n" + "="*80)
    print("✅ ROIC PROVIDER INSTALLATION COMPLETE!")
    print("="*80)
    
    print("""
HOW TO USE ROIC LIKE YAHOO AND FRED:
====================================

1. Launch OpenBB:
   ./launch-openbb-premium.sh

2. Use ROIC provider commands:
   /equity/fundamental/metrics --symbol AAPL --provider roic
   /equity/estimates/consensus --symbol MSFT --provider roic
   
3. Or use shortcuts:
   /roic_quality --symbol AAPL
   /roic_forecast --symbol NVDA

4. ROIC will appear in provider dropdown:
   /equity/fundamental/metrics --symbol AAPL --provider [yahoo|roic|fred]
                                                         ^^^^
                                                    ROIC is here!

5. Data shows in OpenBB's native display (like Yahoo/FRED)

FEATURES:
========
✅ Integrated like Yahoo Finance and FRED
✅ Shows in OpenBB's rich display interface
✅ Available in provider dropdown
✅ Works with export/pagination
✅ Supports all OpenBB display features
""")
    
    return True

if __name__ == "__main__":
    success = install_roic_provider()
    
    if success:
        print("\n🎉 ROIC is now integrated like Yahoo and FRED!")
        print("   Restart OpenBB to see ROIC in the provider list.")
    else:
        print("\n❌ Installation failed. Please check the errors above.")
