# Kasuga

### これは何？
Mecab/CaboCha を利用して、形態素解析、及び係り受け解析を行い、その結果を MongoDB へ格納するツールです。

### 動作方法
例） test.txt の内容を解析する場合

```buildoutcfg
kasuga -f test.txt
```
※ -f オプションでファイル名を指定します

### MongoDB 出力先
* DB名：　kasuga
* Collection名：
    * contexts : 形態素解析情報
    * phases : 文節情報
    * words : 単語情報

現仕様では、 localhost の 27017 番ポートの MongoDB のみを出力先としています。

### 出力フォーマット
「私の名前は中野です」を text.txt に記述して入力とすると、下記を MongoDB へ登録します。  

#### Collections : contexts
形態素解析情報を登録します。

```
{
    "_id" : ObjectId("xxxxxxxxxxxxxxxxxxxxxxxx"),
    "Name" : "test.txt",
    "Body" : "私の名前は中野です",  
    "Words" : [
        {
            "surface" : "私",
            "original" : "私",
            "read" : "わたし",
            "position" : [ "名詞", "代名詞", "一般", "*" ],
            "conjugate" : [ "*", "*" ]
        },
        {
            "surface" : "の",
            "original" : "の",
            "read" : "の",
            "position" : [ "助詞", "連体化", "*", "*" ],
            "conjugate" : [ "*", "*" ]
        },
        {
            "surface" : "名前",
            "original" : "名前",
            "read" : "なまえ",
            "position" : [ "名詞", "一般", "*", "*" ],
            "conjugate" : [ "*", "*" ]
        },
        {
            "surface" : "は",
            "original" : "は",
            "read" : "は",
            "position" : [ "助詞", "係助詞", "*", "*" ],
            "conjugate" : [ "*", "*" ]
        },
        {
            "surface" : "中野",
            "original" : "中野",
            "read" : "なかの",
            "position" : [ "名詞", "固有名詞", "地域", "一般" ],
            "conjugate" : [ "*", "*" ]
        },
        {
            "surface" : "です",
            "original" : "です",
            "read" : "です",
            "position" : [ "助動詞", "*", "*", "*" ],
            "conjugate" : [ "特殊・デス", "基本形" ]
        },
    ]
}
```

#### Collections : phases
文節単位で、文節情報を登録します。

```
{
    "_id" : ObjectId("xxxxxxxxxxxxxxxxxxxxxxxx"),
    "Body" : "私の名前は中野です",
    "Independent" : {
        "surface" : "私",
        "original" : "私",
        "read" : "わたし",
        "position" : [ "名詞", "代名詞", "一般", "*" ],
        "conjugate" : [ "*", "*" ]
    },
    "Ancillary" : {
        "surface" : "の",
        "original" : "の",
        "read" : "の",
        "position" : [ "助詞", "連体化", "*", "*" ],
        "conjugate" : [ "*", "*" ]
    },
    "Link" : {
        "surface" : "名前",
        "original" : "名前",
        "read" : "なまえ",
        "position" : [ "名詞", "一般", "*", "*" ],
        "conjugate" : [ "*", "*" ]
    }
}
```

#### Collections : words
単語単位で、単語情報を登録します。

```
{
    "_id" : ObjectId("xxxxxxxxxxxxxxxxxxxxxxxx"),
    "surface" : "私",
    "original" : "私",
    "read" : "わたし",
    "position" : [ "名詞", "代名詞", "一般", "*" ],
    "conjugate" : [ "*", "*" ]
}
```

