# [TranslationWeb](https://aitranslation.azurewebsites.net)

使用Flask框架

### 下載所需的套件
```pip install -r requirements.txt```
### 執行app.py
```python app.py```
### 用sample體驗功能
1. 語音翻譯:  sample.wav\
  輸入語言: Chinese(Traditional)
2. PDF文件翻譯: sample.pdf\
  輸入語言: English
3. 圖片翻譯:  test_image.png\
  輸入語言: English

### 系統架構圖
```mermaid
graph TD
    %% 節點定義
    A[User]
    B[Web Interface]

    F1[Text Translation]
    F2[Image Translation]
    F3[Speech Translation]
    F4[PDF Translation]

    Z[Translated Result]

    %% 流程
    A --> B

    B --> F1
    B --> F2
    B --> F3
    B --> F4

    %% 每個功能的 API 路徑
    F1 -->|Azure Translation API| Z
    F2 -->|Azure Computer Vision API| G2[Image Text]
    G2 -->|Azure Translation API| Z

    F3 -->|Google Speech Recognition API| G3[Speech Text]
    G3 -->|Azure Translation API| Z

    F4 -->|PyPDF2| G4[Extracted Text]
    G4 -->|Azure Translation API| Z

    %% 樣式（可省略）
    style B fill:#cce5ff,stroke:#3399ff,stroke-width:2px
    style Z fill:#d9edf7,stroke:#31708f
```
