# Kodi Rclone 服务插件

此插件将 Rclone 功能集成到 Kodi 中，允许您直接从 Kodi 界面管理和同步文件。Rclone 是一个命令行程序，用于管理云存储上的文件。通过此插件，您可以自动执行任务，例如使用来自各种云服务的内容更新您的 Kodi 媒体库。

## 功能

- 在您的云存储和 Kodi 之间同步文件。
- 自动更新媒体库（仍在开发中）。
- 通过 Rclone 支持各种云服务。
- 适用于 Kodi 21 omega。

## 安装

1. 从 [发布页面](https://github.com/warpirobo/RCLONE-ADDON-KODI-NEXUS-Android-/releases/tag/rclone) 下载插件。
2. 替换 zip 文件中的 rclone.conf 为您自己已经设置好的配置文件。
3. 从 [Rclone 官方下载页面](https://rclone.org/downloads/) 下载适合您设备的 rclone 二进制文件并添加到 zip 文件的 bin 目录，确保为您的 Android TV Box 设备获取 ARM v7 版本。
4. 打开 Kodi 并进入 **附加组件**。
5. 点击 **附加组件浏览器** 图标，然后选择 **从 zip 文件安装**。
6. 导航到下载的 zip 文件并选择它。
7. 等待安装完成。
8. 对于 Android 10 或更高版本的电视盒子，您需要安装修改版本的 Kodi，将 Kodi 的版本号降低到 Android 9。

## 配置

1. 安装后，进入 **附加组件** > **我的附加组件** > **服务**。
2. 选择 **Rclone Service** 然后选择 **配置**。
3. 输入您的 Rclone 配置详细信息。

## 使用

- 要启动 Rclone 服务，进入 **附加组件** > **我的附加组件** > **服务** 并选择 **Rclone Service**。
- 使用提供的脚本自动执行任务，例如更新您的媒体库。

## 支持

如有任何问题或功能请求，请在 [GitHub 仓库](https://github.com/warpirobo/repository/issues) 上打开一个问题。

## 捐赠

如果您发现此插件有用并希望支持其开发，请考虑进行捐赠。您的支持非常感谢！

https://www.paypal.com/paypalme/ITARIOS

---

*注意：此插件与官方 Kodi 团队无关联或认可。*
