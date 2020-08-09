# ansible-role-authenticate [![Build Status](https://travis-ci.org/izumimatsuo/ansible-role-authenticate.svg?branch=master)](https://travis-ci.org/izumimatsuo/ansible-role-authenticate)

Linux ユーザ管理機能を設定する ansible role です

標準で以下の設定を実施

- 公開鍵認証
- ユーザ追加および公開鍵登録
- グループ追加（一般グループ、管理グループ）
- sudo設定（管理グループへの追加）
- 無効ユーザ削除

二段階認証の設定可能（```enable_two_step_auth``` を yes に設定）

- 公開鍵認証＋UNIX パスワード認証
- 公開鍵認証＋google_authenticator によるワンタイムパスワード認証

UNIX パスワード認証を利用するにあたって、セキュリティポリシーの設定可能

ワンタイムパスワードの利用

1. 公開鍵認証＋UNIX パスワード認証でログインする
1. google-authenticator コマンドを実行する
1. 実行後に二次元バーコードが表示される
1. google-authenticator アプリを起動したスマートフォンで上記バーコードを読み取る
1. 以降は、google-authenticator アプリに表示されるワンタイムパスワードを使ってログインする

## 設定項目

以下の設定項目は上書き可能

| 項目名               | デフォルト値 | 説明                                           |
| -------------------- | ------------ | ---------------------------------------------- |
| users                | []           | ユーザ追加情報（後述）                         |
| user_group           | maintainer   | 一般ユーザグループ名                           |
| admin_group          | adminuser    | 管理ユーザグループ名                           |
| enable_term_logging  | yes          | 操作ログ記録の有無                             |
| enable_two_step_auth | no           | 二段階認証設定有無                             |
| only_public_key_user | none         | 二段階認証回避（公開鍵認証のみ許可）するユーザ |
| passwd_expiration    | 99999        | パスワード有効期間（日数）                     |
| passwd_quality       | none         | パスワードポリシー（後述）                     |

### ユーザ追加情報

追加するユーザ毎に以下の項目を設定する

| 項目名     | 説明                                   |
| ---------- | -------------------------------------- |
| name       | ユーザ名                               |
| public_key | 公開鍵                                 |
| sudoers    | 管理ユーザに設定する場合 yes（省略可） |

設定例

```
users:
    - name: taro
      public_key: 'ssh-rsa AAAA...'
    - name: jiro
      public_key: 'ssh-rsa AAAA...'
      sudoers: yes
```

### パスワードポリシー

以下の項目を組み合わせて設定する

| 項目名         | デフォルト値 | 説明 |
| -------------- | ------------ | ---- |
| difok          | 5            | 変更前のパスワードに含まれる文字が変更後のパスワードに N 文字以上含まれてはならない |
| minlen         | 9            | パスワードの最低文字数。6文字未満には設定できない |
| dcredit        | 1            | パスワード内に必要とする数字の数 |
| ucredit        | 1            | パスワード内に必要とする英大文字の数 |
| lcredit        | 1            | パスワード内に必要とする英小文字の数 |
| ocredit        | 1            | パスワード内に必要とする記号の数 |
| minclass       | 0            | パスワードの最低文字種類数（数字、大文字、小文字、記号）（0は無効） |
| maxrepeat      | 0            | パスワードで許可される連続する同じ文字の最大数（0は無効） |
| maxclassrepeat | 0            | パスワードで許可される連続する同じ文字種の最大数（0は無効） |

文字種はなんでもいいけど最低文字数は12文字に固定したい場合の例

```
passwd_quality: { minlen: 12, dcredit: 0, ucredit: 0, lcredit: 0, ocredit: 0 }
```

最低文字数は12文字だけど、数字と記号は1文字以上必須にしたい場合の例

```
passwd_quality: { minlen: 12, dcredit: -1, ucredit: 0, lcredit: 0, ocredit: -1 }
```

何文字以上含めるとかは指定せず、とりあえず全部の文字種を含める場合の例

```
passwd_quality: { minlen: 12, minclass: 4 }
```

