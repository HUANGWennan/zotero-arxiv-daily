[中文](#chinese) · [English](#english)

<a name="english"></a>
## English

<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="assets/logo.svg" alt="logo"></a>
</p>

<h3 align="center">Zotero-arXiv-Daily</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  ![Stars](https://img.shields.io/github/stars/TideDra/zotero-arxiv-daily?style=flat)
  [![GitHub Issues](https://img.shields.io/github/issues/TideDra/zotero-arxiv-daily)](https://github.com/TideDra/zotero-arxiv-daily/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/TideDra/zotero-arxiv-daily)](https://github.com/TideDra/zotero-arxiv-daily/pulls)
  [![License](https://img.shields.io/github/license/TideDra/zotero-arxiv-daily)](/LICENSE)

</div>

---

<p align="center"> Recommend new arxiv papers of your interest daily according to your Zotero libarary.
    <br> 
</p>

> [!IMPORTANT]
> Please keep an eye on this repo, and merge your forked repo in time when there is any update of this upstream, in order to enjoy new features and fix found bugs.

## 🧐 About <a name = "about"></a>

> Track new scientific researches of your interest by just forking (and staring) this repo!😊

*Zotero-arXiv-Daily* finds arxiv papers that may attract you based on the context of your Zotero libarary, and then sends the result to your mailbox📮. It can be deployed as Github Action Workflow with **zero cost**, **no installation**, and **few configuration** of Github Action environment variables for daily **automatic** delivery.

## ✨ Features
- Totally free! All the calculation can be done in the Github Action runner locally within its quota (for public repo).
- AI-generated TL;DR for you to quickly pick up target papers.
- Affiliations of the paper are resolved and presented.
- Links of PDF and code implementation (if any) presented in the e-mail.
- List of papers sorted by relevance with your recent research interest.
- Fast deployment via fork this repo and set environment variables in the Github Action Page.
- Support LLM API for generating TL;DR of papers.
- Ignore unwanted Zotero papers using gitignore-style pattern.

## 📷 Screenshot
![screenshot](./assets/screenshot.png)

## 🚀 Usage
### Quick Start
1. Fork (and star😘) this repo.
![fork](./assets/fork.png)

2. Set Github Action environment variables.
![secrets](./assets/secrets.png)

Below are all the secrets you need to set. They are invisible to anyone including you once they are set, for security.

| Key | Required | Type |Description | Example |
| :--- | :---: | :---  | :---  | :--- |
| ZOTERO_ID | ✅ | str  | User ID of your Zotero account. **User ID is not your username, but a sequence of numbers**Get your ID from [here](https://www.zotero.org/settings/security). You can find it at the position shown in this [screenshot](https://github.com/TideDra/zotero-arxiv-daily/blob/main/assets/userid.png). | 12345678  |
| ZOTERO_KEY | ✅ | str  | An Zotero API key with read access. Get a key from [here](https://www.zotero.org/settings/security).  | AB5tZ877P2j7Sm2Mragq041H   |
| ARXIV_QUERY | ✅ | str  | The categories of target arxiv papers. Use `+` to concatenate multiple categories. The example retrieves papers about AI, CV, NLP, ML. Find the abbr of your research area from [here](https://arxiv.org/category_taxonomy).  | cs.AI+cs.CV+cs.LG+cs.CL |
| SMTP_SERVER | ✅ | str | The SMTP server that sends the email. I recommend to utilize a seldom-used email for this. Ask your email provider (Gmail, QQ, Outlook, ...) for its SMTP server| smtp.qq.com |
| SMTP_PORT | ✅ | int | The port of SMTP server. | 465 |
| SENDER | ✅ | str | The email account of the SMTP server that sends you email. | abc@qq.com |
| SENDER_PASSWORD | ✅ | str | The password of the sender account. Note that it's not necessarily the password for logging in the e-mail client, but the authentication code for SMTP service. Ask your email provider for this.   | abcdefghijklmn |
| RECEIVER | ✅ | str | The e-mail address that receives the paper list. | abc@outlook.com |
| MAX_PAPER_NUM | | int | The maximum number of the papers presented in the email. This value directly affects the execution time of this workflow, because it takes about 70s to generate TL;DR for one paper. `-1` means to present all the papers retrieved. | 50 |
| SEND_EMPTY | | bool | Whether to send an empty email even if no new papers today. | False |
| USE_LLM_API | | bool | Whether to use the LLM API in the cloud or to use local LLM. If set to `1`, the API is used. Else if set to `0`, the workflow will download and deploy an open-source LLM. Default to `0`. | 0 |
| OPENAI_API_KEY | | str | API Key when using the API to access LLMs. You can get FREE API for using advanced open source LLMs in [SiliconFlow](https://cloud.siliconflow.cn/i/b3XhBRAm). | sk-xxx |
| OPENAI_API_BASE | | str | API URL when using the API to access LLMs. If not filled in, the default is the OpenAI URL. | https://api.siliconflow.cn/v1 |
| MODEL_NAME | | str | Model name when using the API to access LLMs. If not filled in, the default is gpt-4o. Qwen/Qwen2.5-7B-Instruct is recommended when using [SiliconFlow](https://cloud.siliconflow.cn/i/b3XhBRAm). | Qwen/Qwen2.5-7B-Instruct |

There are also some public variables (Repository Variables) you can set, which are easy to edit.
![vars](./assets/repo_var.png)

| Key | Required | Type | Description | Example |
| :--- | :---  | :---  | :--- | :--- |
| ZOTERO_IGNORE | | str | Gitignore-style patterns marking the Zotero collections that should be ignored. One rule one line. Learn more about [gitignore](https://git-scm.com/docs/gitignore). | AI Agent/<br>**/survey<br>!LLM/survey |
| REPOSITORY | | str | The repository that provides the workflow. If set, the value can only be `TideDra/zotero-arxiv-daily`, in which case, the workflow always pulls the latest code from this upstream repo, so that you don't need to sync your forked repo upon each update, unless the workflow file is changed. | `TideDra/zotero-arxiv-daily` |
| REF | | str | The specified ref of the workflow to run. Only valid when REPOSITORY is set to `TideDra/zotero-arxiv-daily`. Currently supported values include `main` for stable version, `dev` for development version which has new features and potential bugs. | `main` |

That's all! Now you can test the workflow by manually triggering it:
![test](./assets/test.png)

> [!NOTE]
> The Test-Workflow Action is the debug version of the main workflow (Send-emails-daily), which always retrieve 5 arxiv papers regardless of the date. While the main workflow will be automatically triggered everyday and retrieve new papers released yesterday. There is no new arxiv paper at weekends and holiday, in which case you may see "No new papers found" in the log of main workflow.

Then check the log and the receiver email after it finishes.

By default, the main workflow runs on 22:00 UTC everyday. You can change this time by editting the workflow config `.github/workflows/main.yml`.

### Local Running
Supported by [uv](https://github.com/astral-sh/uv), this workflow can easily run on your local device if uv is installed:
```bash
# set all the environment variables
# export ZOTERO_ID=xxxx
# ...
cd zotero-arxiv-daily
uv run main.py
```
> [!IMPORTANT]
> The workflow will download and run an LLM (Qwen2.5-3B, the file size of which is about 3G). Make sure your network and hardware can handle it.

> [!WARNING]
> Other package managers like pip or conda are not tested. You can still use them to install this workflow because there is a `pyproject.toml`, while potential problems exist.

## 🚀 Sync with the latest version
This project is in active development. You can subscribe this repo via `Watch` so that you can be notified once we publish new release.

![Watch](./assets/subscribe_release.png)


## 📖 How it works
*Zotero-arXiv-Daily* firstly retrieves all the papers in your Zotero libarary and all the papers released in the previous day, via corresponding API. Then it calculates the embedding of each paper's abstract via an embedding model. The score of a paper is its weighted average similarity over all your Zotero papers (newer paper added to the libarary has higher weight).

The TLDR of each paper is generated by a lightweight LLM (Qwen2.5-3b-instruct-q4_k_m), given its title, abstract, introduction, and conclusion (if any). The introduction and conclusion are extracted from the source latex file of the paper.

## 📌 Limitations
- The recommendation algorithm is very simple, it may not accurately reflect your interest. Welcome better ideas for improving the algorithm!
- This workflow deploys an LLM on the cpu of Github Action runner, and it takes about 70s to generate a TLDR for one paper. High `MAX_PAPER_NUM` can lead the execution time exceed the limitation of Github Action runner (6h per execution for public repo, and 2000 mins per month for private repo). Commonly, the quota given to public repo is definitely enough for individual use. If you have special requirements, you can deploy the workflow in your own server, or use a self-hosted Github Action runner, or pay for the exceeded execution time.

## 👯‍♂️ Contribution
Any issue and PR are welcomed! But remember that **each PR should merge to the `dev` branch**.

## 📃 License
Distributed under the AGPLv3 License. See `LICENSE` for detail.

## ❤️ Acknowledgement
- [pyzotero](https://github.com/urschrei/pyzotero)
- [arxiv](https://github.com/lukasschwab/arxiv.py)
- [sentence_transformers](https://github.com/UKPLab/sentence-transformers)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)

## ☕ Buy Me A Coffee
If you find this project helpful, welcome to sponsor me via WeChat or via [ko-fi](https://ko-fi.com/tidedra).
![wechat_qr](assets/wechat_sponsor.JPG)


## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=TideDra/zotero-arxiv-daily&type=Date)](https://star-history.com/#TideDra/zotero-arxiv-daily&Date)

---

<a name="chinese"></a>
## 中文

根据你的 Zotero 文献库推荐每日 arXiv 新论文并通过邮件发送。列表按相关性排序，包含简短 AI 摘要、可解析的作者机构、PDF 链接及可用的代码链接。可用类 gitignore 规则排除不相关的 Zotero 分类。项目可在 GitHub Actions 或本机运行，云端模型 API 为可选项。

### GitHub Actions 部署

1. Fork 此仓库，进入 **Settings → Secrets and variables → Actions**。在 **Secrets** 填写下表所需参数；不要把密钥或邮箱密码提交到仓库。
2. 在 **Actions** 手动运行 **Test-Workflow**，检查日志和收件箱。测试工作流固定提取 5 篇。主流程每日默认 UTC 22:00 运行，查前一天新发布的论文，可通过 [工作流](.github/workflows/main.yml) 调整。周末及假期可能没有新论文。
3. 可订阅上游更新。有需要时同步 fork。以 `REPOSITORY=TideDra/zotero-arxiv-daily` 运行上游代码时，可用 `REF=main` 或 `REF=dev` 指定分支；工作流文件本身的改动仍需同步。

| 参数 | 是否必填 | 用途 |
| --- | --- | --- |
| `ZOTERO_ID` | 是 | Zotero **数字**用户 ID，不是用户名 |
| `ZOTERO_KEY` | 是 | 对应文献库的只读 API 密钥；在 [Zotero 安全设置](https://www.zotero.org/settings/security) 创建 |
| `ARXIV_QUERY` | 是 | [arXiv 学科代码](https://arxiv.org/category_taxonomy)，用 `+` 拼接，例如 `cs.AI+cs.LG` |
| `SMTP_SERVER`、`SMTP_PORT` | 是 | 邮箱服务商的 SMTP 地址和端口 |
| `SENDER`、`SENDER_PASSWORD`、`RECEIVER` | 是 | 发件地址、SMTP 验证凭据（如应用专用密码）、收件地址 |
| `MAX_PAPER_NUM`、`SEND_EMPTY` | 否 | 邮件论文数上限（`-1` 不限制）、没有论文是否也发邮件 |
| `USE_LLM_API`、`OPENAI_API_KEY`、`OPENAI_API_BASE`、`MODEL_NAME` | 否 | 是否改用云端 API，以及相应密钥、地址和模型；默认使用本地模型 |
| `ZOTERO_IGNORE` | 否 | 要忽略的 Zotero 分类；每行一条 gitignore 风格规则，设为 Repository Variable |

### 本地运行、原理与限制

安装 [uv](https://github.com/astral-sh/uv)，通过环境变量配置相同参数，在仓库根目录运行 `uv run main.py`。默认本地摘要模型约 3 GB，请预留磁盘、网络和运行时间；其他包管理器未经过同等测试。

相关性根据摘要的向量相似度计算，较晚加入 Zotero 的文献权重更高。摘要模型使用标题、摘要以及可提取的引言和结论。排序是启发式结果，不保证完全符合兴趣；CPU 上为每篇文章生成摘要可能较慢。可降低 `MAX_PAPER_NUM`，或使用自己的 runner / 主机，避免触及 GitHub Actions 的运行限制。

贡献代码时按上游约定以 `dev` 为目标分支。项目采用 [AGPLv3](LICENSE)。上游演示截图、依赖致谢和赞助入口保留于英文原文。
