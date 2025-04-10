# AI-personal-project---8-puzzle-game

## Mục lục

- [1. Giới thiệu bài toán](#1-giới-thiệu-bài-toán)
- [2. Một số thuật toán sử dụng](#2-một-số-thuật-toán-sử-dụng)
  - [2.1. Tìm kiếm không có thông tin](#21-tìm-kiếm-không-có-thông-tin)
    - [Thuật toán BFS](#thuật-toán-bfs)
    - [Thuật toán DFS](#thuật-toán-dfs)
    - [Thuật toán IDS](#thuật-toán-ids)
  - [2.2. Tìm kiếm có thông tin](#22-tìm-kiếm-có-thông-tin)
    - [Thuật toán Greedy](#thuật-toán-greedy)
    - [Thuật toán A](#thuật-toán-a)
    - [Thuật toán Iterative deepening a](#thuật-toán-iterative-deepening-a)
  - [2.3. Thuật toán leo đồi](#23-thuật-toán-leo-đồi)
    - [Thuật toán Simple hill climbing](#thuật-toán-simple-hill-climbing)
    - [Thuật toán Steppest ascent hill climbing](#thuật-toán-steppest-ascent-hill-climbing)
    - [Thuật toán Stochastic hill climbing](#thuật-toán-stochastic-hill-climbing)

## 1. Giới thiệu bài toán
Bài toán 8 puzzle có trạng thái ban đầu là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống).

Bài toán 8 puzzle có trạng thái mục tiêu cũng là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống).

Yêu cầu đặt ra của bài toán là di chuyển số 0 (ô trống) theo 1 trong các hướng (hành động) lên, xuống, trái, phải sao cho từ trạng thái ban đầu đạt được trạng thái mục tiêu qua 1 số bước chuyển đổi ô trống.

Tùy thuộc vào thuật toán sử dụng, ta có thể tìm ra lời giải là đường đi từ trạng thái ban đầu đầu đến trạng thái mục tiêu trải qua số bước, thời gian giải, không gian trạng thái mở rộng có thể khác nhau, thậm chí có một số trường hợp một toán có thể không tìm ra được lời giải.

## 2. Một số thuật toán sử dụng
Xét trạng thái đầu vào và trạng thái mục tiêu như hình sau:
![image](assets/start and end state.png)

### 2.1. Tìm kiếm không có thông tin
##### Thuật toán BFS
![Error](gif/BFS.gif)

##### Thuật toán DFS
![Error](gif/DFS.gif)

##### Thuật toán IDS
![Error](gif/IDS.gif)

### 2.2. Tìm kiếm có thông tin
##### Thuật toán Greedy
![Error](gif/Greedy.gif)

##### Thuật toán A*
![Error](gif/Astart.gif)

##### Thuật toán Iterative deepening a*
![Error](gif/IDAstart.gif)

### 2.3. Thuật toán leo đồi
##### Thuật toán Simple hill climbing
![Error](gif/SHC.gif)

##### Thuật toán Steppest ascent hill climbing
![Error](gif/SAHC.gif)

##### Thuật toán Stochastic hill climbing
