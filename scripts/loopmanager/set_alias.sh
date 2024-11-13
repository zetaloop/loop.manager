# Set alias "lom" for Loop Manager

# 检查并移除已存在的alias
if grep -q "alias lom=" ~/.bashrc; then
    sed -i '/alias lom=/d' ~/.bashrc
fi

# 添加新的alias
echo "alias lom='python3 $CWD/lom.py' # Loop.Manager" >> ~/.bashrc

echo ====[Modifying Finished]====
echo
echo Please run "source ~/.bashrc" to apply the changes.
echo
echo To start Loop.Manager, run: lom.
echo
