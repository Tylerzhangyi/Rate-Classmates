# Overleaf 编译设置说明

## 更改编译器为 XeLaTeX

在 Overleaf 中，按以下步骤更改编译器：

1. **打开编译器设置**：
   - 点击 Overleaf 编辑器顶部的 "Menu"（菜单）按钮
   - 或者点击左上角的 "Menu" 图标（三条横线）

2. **选择编译器**：
   - 在菜单中找到 "Settings"（设置）
   - 在 "Compiler"（编译器）下拉菜单中选择 **"XeLaTeX"**
   - 点击 "Recompile"（重新编译）按钮

3. **编译文档**：
   - 点击编辑器顶部的 "Recompile" 按钮
   - 等待编译完成，PDF 将自动更新

## 注意事项

- **必须使用 XeLaTeX**：因为文档使用了 `fontspec` 和 `xeCJK` 包来支持中文
- **不要使用 pdfLaTeX**：pdfLaTeX 不支持 `fontspec` 包
- **编译可能需要多次**：LaTeX 文档通常需要编译两次才能正确生成引用和目录

## 替代方案（如果 XeLaTeX 不可用）

如果 Overleaf 不支持 XeLaTeX，可以改用 LuaLaTeX：
- 在编译器设置中选择 "LuaLaTeX"
- 文档应该也能正常编译

