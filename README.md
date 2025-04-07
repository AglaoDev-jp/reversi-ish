
---

# リバーシ”風”ゲームv1
  
コード作成、テキスト作成、画像生成にChatGPTを使用しています。  
このリポジトリでは、ゲームの**ソースコード**を公開しています。  
ゲームファイル(実行ファイル)のダウンロードは[こちら](https://github.com/AglaoDev-jp/reversi-ish/releases/download/v1.0/reversi-ish_v1.zip)  
ゲームのあそびかたは[こちら](./README_GAME.md)  

---

本プロジェクトの制作にあたり、OpenAIの対話型AI「ChatGPT」のサポートを受けて、画像生成、アイデア出し、コード修正、文章の表現の改善などをスムーズに行うことができました。開発に携わったすべての研究者、開発者、関係者の皆様に、心より感謝申し上げます。    

---

## ゲームファイル(実行ファイル)のセキュリティに関する注意事項
本ソフトウェアは、**悪意のあるコード（ウイルス・マルウェア）は含まれていません。**  
しかし、一部のアンチウイルスソフトにより、**誤検出**されることがあります。  

### ** 誤検出が起こる理由**
- **圧縮やパッキング処理を行っていること**
- **デジタル署名がないこと**

これらの要因により、一部のウイルス対策ソフトが誤って「疑わしい」と判断することがあります。  

### **安全性を確認する方法**
本ソフトウェアが安全かどうかを確認する場合は、以下の方法を推奨します：
- **[VirusTotal](https://www.virustotal.com/)にアップロードし、スキャン結果を確認する** 
- **仮想環境（VirtualBox, Windows Sandbox など）で実行してみる**
- **公式の配布元（GitHub）からダウンロードする**

### **※誤検出が気になる場合や、安全性に不安がある場合は、ダウンロードや実行を控えてください。**

---

## 免責事項
本ゲームの利用や環境設定に起因するいかなる損害や不具合について、作者は一切の責任を負いません。  

---

**製作期間**

- **v1**: 2025年3月27日 ~ 2025年4月3日

---

※ このリポジトリは個人学習のために使用しています。そのため、プルリクエスト（Pull Request）は、お受けすることができません。ご了承ください。  

---

## 使用言語とライブラリ

### 使用言語
- **Python 3.12.5**

### 使用モジュール・ライブラリ
#### 標準モジュール

- **sys** - `Pygame`の`sys.exit()` によるプログラムの終了処理に使用。
- **random** - 疑似乱数を生成。AIの石選択ロジックに使用。
- **pathlib** - ファイルパスの操作に使用。

#### 外部ライブラリ

- **Pygame** – ゲーム画面の描画やイベント処理など、GUIを実現するために使用。

### 実行ファイル化
- **PyInstaller** – Pythonスクリプトを単一の実行ファイル（.exeなど）に変換するために使用。

### 使用エディター
- **Visual Studio Code (VSC)** – コーディングおよびデバッグに使用。  

---

### 著作権表示とライセンス
 
### **Python**  
- © Python Software Foundation  
Licensed under the Python Software Foundation License (PSF License).  
[Python license](https://docs.python.org/3/license.html)  
- またはフォルダ内の [LICENSE-PSF.txt](./licenses/LICENSE-PSF.txt) をご確認ください。  
※ コードのみであればライセンス添付は不要ですが、PyInstallerを使って実行ファイル化する際にはPythonのライセンス（PSF License）の添付が必要です。  
   (内部にPythonの一部が組み込まれるため)
※ Python 3.8.6以降、PSF LicenseとZero-Clause BSDライセンスのデュアルライセンスとなっていますが、
  これはドキュメント内のコード例やレシピ、その他のコードを使用する場合に必要となるようです。  
  通常の使用であれば PSF License のみで大丈夫みたいです。

---

### このプロジェクトでは、以下のオープンソースライブラリを使用しています：

#### **Pygame**
- © 2000-2023 Pygame developers  

Pygameは、**GNU Lesser General Public License バージョン2.1 (LGPL v2.1)** の下でライセンスされています。  
このライセンスでは、以下の条件を満たす必要があります：  
- **ライセンス文を配布物に含めること。**  
- **ライブラリを改変した場合、その改変部分のソースコードを公開すること。（可能であれば改変内容を Pygame プロジェクトにフィードバックすることが推奨されています）**  
LGPL v2.1 により、Pygameは商用・非商用を問わず自由に利用・再配布することができます。  

### **PyInstallerを使った場合の対応**
- PyInstallerを使用してPygameをバンドルした場合でも、LGPLライセンスの条件を満たしています。  
  - ライブラリは動的リンクとして扱われます。
  - アプリケーションのソースコードを公開する義務はありません。
- ただし、以下の対応を行う必要があります：  
  - ライセンス文を配布パッケージに含める。  
  - Pygameを改変した場合、その改変部分のソースコードを公開する。  

詳細なライセンス条項については、以下を参照してください：  
- [Pygame License](https://github.com/pygame/pygame/blob/main/docs/LGPL.txt)  
- プロジェクト内の [LGPL.txt](./licenses/third_party/LGPL v2.1.txt)  

> **備考:** PyInstallerでバンドルされた場合、ユーザーがライブラリを差し替える権利は担保されています。そのため、アプリケーション全体をオープンソースにする必要はありません。
### 静的リンクとの違い  
### **LGPLの基本ルール**
- 動的リンクが原則

  LGPLライセンスでは、ライブラリをアプリケーションに「動的リンク」することが前提です。  
  動的リンクとは、実行時にライブラリを別ファイルとして参照する方法を指します（例: .dll, .so）  
  LGPLライセンスでは、Pygameをリンクしているアプリケーションのソースコードを公開する必要はありません。  
  ただし、利用者がライブラリを差し替えられる仕組みを提供する必要があります。  

  Pygameを「静的リンク」してアプリケーションに組み込んだ場合、LGPLライセンスの適用範囲が広がり、  
  アプリケーション全体にLGPLが適用される可能性があります。  

- 静的リンク
  - 静的リンクでは、ライブラリのコードがアプリケーションのバイナリに直接埋め込まれるため、ライブラリの差し替えができなくなります。  
  この場合、アプリケーション全体がLGPLの影響を受ける可能性があります。

- 動的リンク（PyInstallerのケース）
  - PyInstallerはライブラリを個別のモジュールとして扱うため、実行時に動的にロードされます。
  この形式は、技術的にはPyInstallerで作成された実行ファイルの依存ライブラリ（例: Pygameの.dllファイル）を他のバージョンや改変版に置き換えることが可能です。  
  このため、アプリケーションがクローズドソースでも配布が可能のようです。　　
  
---

#### **PyInstaller**  
このプロジェクトは、PyInstallerを使用して実行ファイル化に対応しています。  
PyInstallerはGPLライセンスですが、例外規定により`生成される実行ファイル自体はGPLの制約を受けません`。

詳しくは以下をご確認ください：  
- [PyInstaller公式ライセンス情報](https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt)  

---

## フォントについて

- このコードではPC内の`Meiryo`を参照する形で記述しています。プロジェクト内にフォントファイルは存在しません。  
- 環境によっては正しく文字が表示されない場合があります。  

---

これらのプロジェクトの開発者および貢献者の皆様に、心より感謝申し上げます。

---

### 問題点
- 音楽や効果音が未実装です。
- 難易度は「やさしい」と「ふつう」の2種類のみです。
- AIのアルゴリズムが単純(位置に重みをつけてスコア評価 → 同点ならランダムで選ぶ)で、強くありません。
- フォントをPC内の「Meiryo」で参照する記述をしており、環境によって表示が異なる場合があります。
- 黒がパスした後、一部の状況でAIが動作しなくなることがあります。

---

## ソースコードについて

1. **Pythonのインストール**  
   `.py`ファイルの実行には、Pythonがインストールされている環境が必要です。

### 必要なライブラリのインストール

   - インストールがまだの場合は、以下のコマンドを使用してください。
   
   Pygameのインストール
   ```shell
   pip install pygame
   ```

   PyInstallerのインストール
   ```shell
   pip install pyinstaller
   ```

4. **ゲームの起動**  
   コマンドラインインターフェースを使用して、以下の手順でゲームを起動します。

   - `cd`コマンドで`reversi-ish_v1.py`ファイルのディレクトリに移動します。  
   例: `reversi-ish_v1.py`ファイルを右クリックして「プロパティ」の「場所」をコピーなど。  
   ```shell
   # 例: デスクトップにフォルダがある場合 (パスはPC環境により異なります)
   cd "C:\..\..\Desktop\reversi-ish_v1"
   ```

   - フォルダに移動後、以下のコマンドでゲームを起動します。  
   ```shell
   python reversi-ish_v1.py
   ```

5. **コードエディターでの実行**  
   一部のコードエディター（VSCなど）では、直接ファイルを実行することが可能です。  
     
---

## PyInstallerによる実行ファイル化

このソースコードでは、**PyInstaller**を使用してPythonスクリプトを単一の実行ファイルに変換して使用することができました。  
この手順を実施することで、Python環境をインストールしていない環境でもゲームを実行できるようになります。配布にも適した形に仕上げることが可能です。  
以下に手順を示します：  

ディレクトリ構成：  

```

プロジェクトフォルダ/            
├── reversi-ish_v1.py               <- メインコード
├── image.png             <- スタート画面の画像
└── icon.ico              <- アイコン画像（任意）

```

---

### 必要なライブラリのインストール

**依存ライブラリのインストール**  


   Pygameのインストール
   ```shell
   pip install pygame
   ```
   
   PyInstallerのインストール
   ```shell
   pip install pyinstaller
   ```

---

### 実行ファイルの作成方法

1. **プロジェクトフォルダに移動する**  
   コマンドプロンプトまたはターミナルで、プロジェクトフォルダに移動します：

   ```shell
   cd <プロジェクトフォルダのパス>
   ```

   **例**: デスクトップにフォルダがある場合  
   ```shell
   cd C:\Users\<ユーザー名>\Desktop\reversi-ish_v1
   ```

2. **実行ファイルの作成**  
   以下のコマンドを実行します：

   ```shell
    pyinstaller --clean --onefile --windowed --icon=icon.ico --add-data "image.png;." reversi-ish_v1.py


   ```

### オプションの詳細説明

- **`--onefile`**: 単一の .exe ファイルにまとめます。
- **`--windowed`**: コンソールを表示しない。
- **`--icon=icon.ico`**: アプリのアイコンを設定します。
- **`--add-data "image.png;.`**: image.png を .exe と同じフォルダに配置するよう指示(--add-data "ファイル名;出力先")


### 実行ファイルの確認

PyInstallerが成功すると、以下のようなディレクトリ構成が作成されます：

```
プロジェクトフォルダ/
├── build/           <- 一時ファイル（削除してOK）
├── dist/            <- 実行ファイルが保存されるフォルダ
│   └── reversi-ish_v1.exe <- 出来上がった実行ファイル
├── reversi-ish_v1.py          <- メインコード
├── image.png        <- スタート画面の画像
├── icon.ico         <- アイコン画像
└── *.spec           <- PyInstallerの設定ファイル（削除してOK）

```

実行ファイルは`dist`フォルダ内に出力されます。  
`dist`フォルダ内に作成された実行ファイル（例: `reversi-ish_v1.exe`）を使用してゲームを実行できます。  
生成された実行ファイルは、Python環境を必要とせずに動作します。  
ひとつのシステムファイルにまとめられていますので、配布にも適した形になっています。  
distフォルダ内に作成された実行ファイルをそのまま配布するだけで、他のユーザーがゲームをプレイできるようになります。  

### 注意事項

- **セキュリティに関する注意**  
  PyInstallerはスクリプトを実行ファイルにまとめるだけのツールであり、コードの暗号化や高度な保護機能を提供するものではありません。  
  そのため、悪意のあるユーザーが実行ファイルを解析し、コードやデータを取得する可能性があります。  
  コードやデータなどにセキュリティが重要なプロジェクトで使用する場合は、追加の保護手段を検討してください。  

- **OSに応じた調整**  
  MacやLinux環境で作成する場合、`--add-data` オプションのセパレータやアイコン指定の書式が異なるようです。  
  詳細は[PyInstaller公式ドキュメント](https://pyinstaller.org)をご確認ください。  
  実行ファイル化において発生した問題は、PyInstallerのログを確認してください。  

- **ライセンスとクレジットに関する注意**   
    **推奨事項**  
     PyInstallerのライセンスはGPLv2（GNU General Public License Version 2）ですが、例外的に商用利用や非GPLプロジェクトでの利用を許可するための追加条項（特別例外）が含まれています。  
     実行ファイルを配布するだけであれば、PyInstallerの特別例外が適用されるため、GPLv2ライセンスの条件に従う必要はないようです。
     ライセンス条件ではありませんが、プロジェクトの信頼性を高めるため、READMEやクレジットに「PyInstallerを使用して実行ファイルを作成した」旨を記載することを推奨します。  

    **PyInstallerのライセンスが必要な場合**  
     PyInstallerのコードをそのまま再配布する場合、もしくは改変して再利用する場合は、GPLv2ライセンスに従う必要があります。  
     この場合、以下を実施してください：  
      - PyInstallerのライセンス文を同梱する。  
      - ソースコードを同梱するか、ソースコードへのアクセス手段を提供する。  

    **詳細情報**  
     PyInstallerのライセンスについて詳しく知りたい場合は、[公式リポジトリのLICENSEファイル](https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt)をご参照ください。  

---

## このゲームのライセンス

- **このゲームのコード**: MIT License。詳細は[LICENSE-CODE](./licenses/game/LICENSE-CODE)ファイルを参照してください。
- **画像**: Creative Commons Attribution 4.0 (CC BY 4.0)。詳細は[LICENSE-IMAGES](./licenses/game/LICENSE-IMAGES)ファイルを参照してください。

## ライセンスの簡単な説明

- **このゲームのコード**: （MIT License）
このゲームのコードは、MITライセンスのもとで提供されています。自由に使用、改変、配布が可能ですが、著作権表示とライセンスの文言を含める必要があります。

- **画像**: （Creative Commons Attribution 4.0, CC BY 4.0）
このゲームの画像は、CC BY 4.0ライセンスのもとで提供されています。自由に使用、改変、配布が可能ですが、著作権者のクレジットを表示する必要があります。

※これらの説明はライセンスの概要です。詳細な内容は各ライセンスの原文に準じます。

---

## クレジット表示のテンプレート（例）  

### コード
```plaintext
Code by AglaoDev-jp © 2025, licensed under the MIT License.
```

### 画像
```plaintext
Image by AglaoDev-jp © 2025, licensed under CC BY 4.0.
```

---
#### ライセンスの理由
現在のAI生成コンテンツの状況を踏まえ、私は本作品を可能な限りオープンなライセンス設定になるように心がけました。  
問題がある場合、状況に応じてライセンスを適切に見直す予定です。  

このライセンス設定は、権利の独占を目的とするものではありません。明確なライセンスを設定することにより、パブリックドメイン化するリスクを避けつつ、自由な利用ができるように期待するものです。  
  
© 2025 AglaoDev-jp

