
# Add th efollowing to your ~/.zshrc file for pyenv tags in your terminal

# Note: ohmyzsh might delete the contents of your file
# so you'll have to add this after installing ohmyzsh

if command -v pyenv 1>/dev/null 2>&1; then
    eval "$(pyenv init -)"
fi
export PATH=/urs/local/bin:$PATH
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"