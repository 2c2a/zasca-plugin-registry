# ZASCA Plugin Registry

ZASCA 插件仓库 - 存储插件地址信息，开发者可通过 PR 更新。

## 插件列表格式

`plugins.json` 中每个插件包含以下字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 插件显示名称 |
| `description` | string | 是 | 插件简介 |
| `repository` | string | 是 | 插件 GitHub 仓库地址 |
| `version` | string | 是 | 插件最新版本号 |

## 如何提交插件

1. Fork 本仓库
2. 编辑 `plugins.json`，在 `plugins` 对象中添加你的插件信息
3. 提交 Pull Request

### 示例

```json
{
  "my_plugin": {
    "name": "My Plugin",
    "description": "一个示例插件",
    "repository": "https://github.com/username/my-plugin",
    "version": "1.0.0"
  }
}
```

## 通过命令行安装插件

```bash
uv run manage.py plugins install <插件名>
uv run manage.py plugins search <关键词>
uv run manage.py plugins login
```
