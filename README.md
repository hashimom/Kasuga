# Kasuga

## これは何？
KNP を利用して、形態素解析、及び係り受け解析を行い、その結果を辞書型で返すツールです。  
動作には、KNP、及び pyknp が必要です。

## 動作方法
例） test.txt の内容を解析する場合

```buildoutcfg
kasuga -f test.txt
```
※ -f オプションでファイル名を指定します

## 出力フォーマット
「私の名前は中野です」を text.txt に記述して入力とすると、下記の辞書型を返します。


```
{
    "Body" : "私の名前は中野です",
    "Chunks" : [
        {
            "Independent" : {
                "surface" : "私",
                "original" : "私",
                "read" : "わたし",
                "position" : [ '名詞', '普通名詞' ],
                "conjugate" : [ "*", "*" ]
            },
            "Ancillary" : {
                "surface" : "の",
                "original" : "の",
                "read" : "の",
                "position" : [ '助詞', '接続助詞' ],
                "conjugate" : [ "*", "*" ]
            },
            "Link" : {
                "surface" : "名前",
                "original" : "名前",
                "read" : "なまえ",
                "position" : [ '名詞', '普通名詞' ],
                "conjugate" : [ "*", "*" ]
            }
        },
        {
            ・・・・・
        },
        ・・・・・
    ]
}
```
