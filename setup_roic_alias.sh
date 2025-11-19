#!/bin/bash
# Setup ROIC command as system-wide alias

echo "Setting up ROIC command alias..."

# Add to .zshrc (macOS default shell)
echo "" >> ~/.zshrc
echo "# ROIC.ai CLI Integration" >> ~/.zshrc
echo "alias roic='/Users/sdg223157/OPBB/roic'" >> ~/.zshrc
echo "alias roic-quality='/Users/sdg223157/OPBB/roic quality'" >> ~/.zshrc
echo "alias roic-forecast='/Users/sdg223157/OPBB/roic forecast'" >> ~/.zshrc
echo "alias roic-compare='/Users/sdg223157/OPBB/roic compare'" >> ~/.zshrc

# Also add to .bashrc if it exists
if [ -f ~/.bashrc ]; then
    echo "" >> ~/.bashrc
    echo "# ROIC.ai CLI Integration" >> ~/.bashrc
    echo "alias roic='/Users/sdg223157/OPBB/roic'" >> ~/.bashrc
    echo "alias roic-quality='/Users/sdg223157/OPBB/roic quality'" >> ~/.bashrc
    echo "alias roic-forecast='/Users/sdg223157/OPBB/roic forecast'" >> ~/.bashrc
    echo "alias roic-compare='/Users/sdg223157/OPBB/roic compare'" >> ~/.bashrc
fi

echo "✅ Aliases added successfully!"
echo ""
echo "To activate immediately, run:"
echo "  source ~/.zshrc"
echo ""
echo "Then you can use ROIC commands from anywhere:"
echo "  roic quality AAPL"
echo "  roic forecast MSFT"
echo "  roic compare AAPL MSFT GOOGL"
echo ""
echo "Or use shortcuts:"
echo "  roic-quality AAPL"
echo "  roic-forecast MSFT"
echo "  roic-compare AAPL MSFT GOOGL"
