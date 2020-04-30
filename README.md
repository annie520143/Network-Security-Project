# 開發流程

1. 各自clone下來，開新的branch寫。

    #### 主要分支 (已經存在的)
    * **master** -> 穩定版 (只有確定要把這個功能加上去才把 **develop** merge到 **origin/master** 上)
    * **develop** -> 測試版 (用來另外再分支出 **feature** )

    #### 次要分支 (自己開發時新建的)
    * **myfeature** -> 新功能 （由 **develop** 直接分支，開發新功能。最後merge回 **develop branch**）

2. 兩個人開發時，記得先`git checkout -b myfeature`，切換到自己的分支(**feature**)，每次寫code...

    1. **PULL** -> `git pull origin develop`，更新本機code 
    2. **Coding** -> 修改完一個新功能，就記得`git add` `git commit`
    3. **Push** -> 切換到**develop branch** (`git checkout develop`) 利用 –no-ff 合併分支 (`git merge --no-ff myfeature`) 再來刪除 **myfeature** 分支(`git branch -d myfeature`) 最後資料上傳 (`git push origin develop`)


---
# 進度
- **4/10**

    - [x] 用feature inverse回去看pca的重要feature有哪些?\
    *(實驗後發現 pca和我們理解的不一樣 不能選重要feature **所以先不管PCA了**)*

    - [x] 嘗試用不同的cluster演算法\
    *(發現 **DBSCAN** 能分出很多群 好像是我們想要的？)*

- **4/17**
    - **預計進度**
        - [ ] 做好preprocessing 讓它能處理任意資料 (主要是**state**的部分 因為之前只針對'FIN', 'CON'兩種state處理)

        - [ ] 把time feature拿掉看看 (驗證time 是否真的是重要的feature?)

        - [ ] 看看DBSCAN的outlier有哪些 (驗證DBSCAN)

        - [ ] 異常分析(把normal 跟 melicious分開 分別下去train 看結果如何)

    - **問題**
        1. DBSCAN離群值怎麼半
        2. 怎麼predict testing data(沒有函式可以叫 dbscan也不能直接顯示群心 寫了一個func -> DBscan_predict 但是不確定那樣對不對)
        3. PCA降為前後的group number怎麼對應
        
        
- **4/24**
    - **完成進度**
        - [ ] 延續上禮拜的clustering, 用DBSCAN做anolamy analysis
        - [ ] 對http封包跟http特徵做anolamy analysis
        - [ ] prepossing, 可以處理有些port value為16進位的問題, 及建造0, 1數量相等的大dataset, 以利training
        - [ ] 簡單了解DL(透過李弘毅線上課程)
        - [ ] 訓練DNN與testing
        
    - **問題與發現**
        1. 剛開始怎麼train，在testing時表現都不佳(不管label_0或label_1 predict結果都是0)，後來發現在training data中，label 0&1 的比例不該差太多，且我們的testing dataset太小，改正這兩個問題後，結果就好超多!!
        2. epoch問題，由於initial value是隨機的，所以若epoch太小，可能會導致parameter無法optimize，故epoch值不能太大(會跑很慢)，也不能太小(可能無法converge)

        3. 每個epoch跑完的accuracy跟最後的[loss, accuracy]有甚麼差別?
        4. 參數該如何調? 應該建構哪樣的神經網路架構?
        5. 有normalize類別變數的正確率高於沒有normalize類別變數的，但是若沒有normalize類別變數，他中間會有一次epoch突然飆升(會部會跟initial有關)
        
     - **DL整理**
        1. 使用的dataset
            - NUSW10000 : 從大dataset取0-10000筆的資料(0多1少，無法為training使用)
            - NUSW20000 : 從大dataset取10001-20000筆的資料(0多1少，無法為training使用)
            - NUSW10000-label0(1) : NUSW10000中只有0(1)的檔案
            - NUSW20000-label0(1) : NUSW20000中只有0(1)的檔案
            - NUSW10000-0 : 從大dataset取前10000筆label為0的資料
            - NUSW10000-1 : 從大dataset取前10000筆label為1的資料
            - NUSW_mix : NUSW10000-0 + NUSW10000-1，共兩萬筆資料
            
        2. 參數(value) `此次只調整過epochs`
            - initial
            - learning rate
            - batch size
            - epochs
            
        3. 參數(function) `此次未調整`
            - activation
            - loss
            - optimizer
            
        4.  此次model都用NUSW_mix下去train，再用NUSW10000和NUSW20000去test，若要進一步分析則可以使用NUSW10000-label0(1)/NUSW20000-label0(1)
        
     - **結果**
---
### *補充：Clone fork 差別*

- **Clone** : 把專案在遠端儲存庫上的所有內容複製到**本地**，建立起**本機儲存庫**及工作目錄

- **Fork** : 把別人專案的遠端儲存庫內容複製一份到自己的**遠端儲存庫**

- **使用方法** : 如果在開發者在GitHub上看到有興趣的專案，可以執行Fork指令，把別人專案的遠端儲存庫複製到自己的遠端儲存庫，再執行Clone指令，把自己遠端儲存庫的整個專案的所有內容（包括各版本）複製到本機端儲存庫。

---
### *參考資料*

- [git branch](https://blog.wu-boy.com/2011/03/git-%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6-branch-model-%E5%88%86%E6%94%AF%E6%A8%A1%E7%B5%84%E5%9F%BA%E6%9C%AC%E4%BB%8B%E7%B4%B9/)

