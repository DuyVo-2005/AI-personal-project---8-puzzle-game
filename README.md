# AI-personal-project---8-puzzle-game

## Mục lục

- [1. Giới thiệu bài toán](#1-giới-thiệu-bài-toán)
- [2. Mục tiêu]
- [3.1. Nội dung]
  - [3. Một số thuật toán sử dụng](#2-một-số-thuật-toán-sử-dụng)
    - [3.1. Tìm kiếm không có thông tin](#21-tìm-kiếm-không-có-thông-tin)
      - [Các thành phần chính của bài toán tìm kiếm]
      - [Thuật toán BFS](#thuật-toán-bfs)
      - [Thuật toán DFS](#thuật-toán-dfs)
      - [Thuật toán IDS](#thuật-toán-ids)
    - [3.2. Tìm kiếm có thông tin](#22-tìm-kiếm-có-thông-tin)
      - [Thuật toán USC - Uniform Cost Search](#thuật-toán-USC---Uniform-Cost-Search)
      - [Thuật toán Greedy](#thuật-toán-greedy)
      - [Thuật toán A](#thuật-toán-a)
      - [Thuật toán Iterative deepening a](#thuật-toán-iterative-deepening-a)
    - [3.3. Thuật toán leo đồi](#23-thuật-toán-leo-đồi)
      - [Thuật toán Simple hill climbing](#thuật-toán-simple-hill-climbing)
      - [Thuật toán Steppest ascent hill climbing](#thuật-toán-steppest-ascent-hill-climbing)
      - [Thuật toán Stochastic hill climbing](#thuật-toán-stochastic-hill-climbing)
      - [Thuật toán Beam Search](#thuật-toán-beam-search)

## 1. Giới thiệu bài toán
Bài toán 8 puzzle có trạng thái ban đầu là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống).

Bài toán 8 puzzle có trạng thái mục tiêu cũng là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống).

Yêu cầu đặt ra của bài toán là di chuyển số 0 (ô trống) theo 1 trong các hướng (hành động) lên, xuống, trái, phải sao cho từ trạng thái ban đầu đạt được trạng thái mục tiêu qua 1 số bước chuyển đổi ô trống.

Tùy thuộc vào thuật toán sử dụng, ta có thể tìm ra lời giải là đường đi từ trạng thái ban đầu đầu đến trạng thái mục tiêu trải qua số bước, thời gian giải, không gian trạng thái mở rộng có thể khác nhau, thậm chí có một số trường hợp một toán có thể không tìm ra được lời giải.

## 2. Mục tiêu
Áp dụng các thuật toán tìm kiếm trí tuệ nhân tạo đã học ở lớp vào giải quyết một vấn đề cụ thể. Từ đó đưa ra những đánh giá về hiệu suất, hiệu quả của từng loại thuật toán về mặt thời gian, không gian trong từng trường hợp cụ thể. Từ đây, hoàn toàn có thể áp dụng các thuật toán này vào các bài toán thực tiễn như tìm đường đi giữa các thành phố, tìm kiếm thông tin nhanh chóng hơn trong kho dữ liệu lớn, lập lịch, học máy... [1]

## 3. Một số thuật toán sử dụng
Xét trạng thái đầu vào và trạng thái mục tiêu như hình sau:

![image](assets/start_and_end_state.png)

### 3.1. Tìm kiếm không có thông tin
##### Các thành phần chính của bài toán tìm kiếm
Bài toán 8 puzzle có trạng thái ban đầu là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu vào bài toán cần giải quyết.

Bài toán 8 puzzle có trạng thái mục tiêu cũng là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu ra của bài toán (là trạng thái muốn có sao khi thực hiện các hành động từ trạng ban đầu).

Tổng chi phí của đường đi từ trạng thái ban đầu đến trạng thái đang xét, thường ký hiệu là g(state) [2, tr. 168]

Giải pháp là một đường đi chứa các trạng thái với trạng thái đầu tiên là trạng thái ban đầu, các trạng thái biến đổi sau khi thực hiện hành động lên trạng thái ban đầu và trạng thái cuối cùng là trạng thái mục tiêu (trạng thái cần tìm).
##### Thuật toán BFS
![Error](gif/BFS.gif)

##### Thuật toán DFS
![Error](gif/DFS.gif)

##### Thuật toán UCS - Uniform Cost Search
![Error](gif/UCS.gif)

##### Thuật toán IDS
![Error](gif/IDS.gif)

##### Hình ảnh so sánh hiệu suất của các thuật toán

##### Nhận xét về hiệu suất của các thuật toán trong nhóm
BFS - Breadth-First Search (Tìm kiếm theo chiều rộng): Khám phá các trạng thái theo mức độ, có thể được dùng khi các hành động có cùng chi phí, đảm bảo tìm được giải pháp ngắn nhất nếu tồn tại giải pháp. Thuật toán này dùng hàng đợi để lưu trữ các trạng thái đang được xét theo nguyên tắc FIFO (vào trước ra trước). Thuật toán kết thúc khi tìm ra lời giải hoặc khi hàng đợi rỗng. [2, tr.175]

DFS - Depth-First Search (Tìm kiếm theo chiều sâu): Khi các hành động có cùng chi phí có thể áp dụng thuật toán này để Khám phá sâu vào các nhánh trước khi quay lại xét nhánh kế tiếp. Thuật toán có thể tìm ra được lời giải nhưng không đảm bảo tìm được giải pháp tối ưu do có thể phải xét hết tất cả các trạng thái trên nhánh không có lời giải, sau đó mới chuyển sang các nhánh khác.

+	UCS - Uniform Cost Search (Tìm kiếm theo chi phí đồng nhất): Mở rộng từ một trạng thái tới trạng thái có chi phí tốt nhất từ trạng thái gốc đến trạng thái đó, đảm bảo tìm được giải pháp tối ưu với chi phí hành trình tìm kiếm là thấp nhất do tính chi phí các nút lân cận và sau đó mới di chuyển đến nút có chi phí tốt nhất.

IDS - Iterative Deepening Search (Tìm kiếm sâu dần): Thuật toán này ‘kết hợp ưu điểm của tìm kiếm theo chiều rộng và chiều sâu, thuật toán tìm kiếm theo chiều sâu từ mức thấp đến mức cao hơn, đến khi tìm ra giải pháp’. Đây là lựa chọn tối ưu với “các bài toán tìm kiếm khi không biết trước độ sâu của lời giải”. [3]

### 3.2. Tìm kiếm có thông tin
##### Các thành phần chính của bài toán tìm kiếm
Bài toán 8 puzzle có trạng thái ban đầu là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu vào bài toán cần giải quyết.

Bài toán 8 puzzle có trạng thái mục tiêu cũng là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu ra của bài toán (là trạng thái muốn có sao khi thực hiện các hành động từ trạng ban đầu).

Giải pháp là một đường đi chứa các trạng thái với trạng thái đầu tiên là trạng thái ban đầu, các trạng thái biến đổi sau khi thực hiện hành động lên trạng thái ban đầu và trạng thái cuối cùng là trạng thái mục tiêu (trạng thái cần tìm).

##### Thuật toán Greedy
![Error](gif/Greedy.gif)

##### Thuật toán A*
![Error](gif/Astart.gif)

##### Thuật toán Iterative deepening a*
![Error](gif/IDAstart.gif)

##### Hình ảnh so sánh hiệu suất của các thuật toán


##### Nhận xét về hiệu suất của các thuật toán trong nhóm
Greedy Search (Tìm kiếm tham lam - tìm kiếm Greedy): Mở rộng trạng thái tới trạng thái có giá trị hàm heuristic tốt nhất (trong đó, hàm heuristic là hàm đánh giá chi phí từ trạng thái đang xét đến trạng đích).

A-Star Search (Tìm kiếm A*): Tìm kiếm bằng cách tính chi phí từ trạng thái ban đầu đến trạng thái hiện tại và ước lượng chi phí từ trạng thái hiện tại đến trạng thái mục tiêu để tìm ra trạng thái tiếp theo có chi phí tốt nhất để di chuyển đến.

IDA-Star ...

### 3.3. Thuật toán leo đồi
##### Các thành phần chính của bài toán tìm kiếm
Bài toán 8 puzzle có trạng thái ban đầu là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu vào bài toán cần giải quyết.

Bài toán 8 puzzle có trạng thái mục tiêu cũng là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu ra của bài toán (là trạng thái muốn có sao khi thực hiện các hành động từ trạng ban đầu).

Giải pháp là một đường đi chứa các trạng thái với trạng thái đầu tiên là trạng thái ban đầu, các trạng thái biến đổi sau khi thực hiện hành động lên trạng thái ban đầu và trạng thái cuối cùng là trạng thái mục tiêu (trạng thái cần tìm).

##### Thuật toán Simple hill climbing
![Error](gif/SHC.gif)

##### Thuật toán Steppest ascent hill climbing
![Error](gif/SAHC.gif)

##### Thuật toán Stochastic hill climbing
![Error](gif/StochasticHillClimbing.gif)

##### Thuật toán Stimulated Annealing
![Error](gif/StimulatedAnnealing.gif)

##### Thuật toán Beam Search
![Error](gif/BeamSearch.gif)

##### Thuật toán Genetic Algorithm
![Error](gif/GeneticAlgorithm.gif)

##### Hình ảnh so sánh hiệu suất của các thuật toán

##### Nhận xét về hiệu suất của các thuật toán trong nhóm
Nhìn chung ơ nhóm thuật toán này, từ một trạng thái hiện tại đanh xét, quá trình tìm kiếm sẽ mở rộng ra các trạng thái lân cận tốt hơn mà không xét hết cây tìm kiếm. Nhược điểm lớn nhất ở nhóm này là quá trình tìm kiếm dễ mắc kẹt tại cực trị địa phương dẫn đến không tìm ra lời giải.

Thuật toán leo đồi đơn giản đánh giá từng trạng thái lân cận một cách tuần tự và chọn trạng thái đầu tiên tối ưu hơn so với trạng thái hiện tại.

Thuật toán leo đồi dốc nhất đánh giá tất cả các trạng thái lân cận và chọn trạng thái mang lại cải thiện lớn nhất so với trạng thái hiện tại.

Thuật toán leo đồi ngẫu nhiên chọn ngẫu nhiên một trạng thái lân cận và quyết định chuyển sang trạng thái đó nếu nó tốt hơn trạng thái hiện tại.

## 4. Tài liệu tham khảo
[1]. Elastic Platform Team, "Understanding AI search algorithms", elastic ,https://www.elastic.co/blog/understanding-ai-search-algorithms, ngày 21 tháng 3 năm 2024 (truy cập ngày 9 tháng 5 năm 2025)
[2]. Russell 2020 Artificial intelligence a modern approach
[3]. https://kdata.vn/tin-tuc/cac-thuat-toan-tim-kiem-chia-khoa-mo-cua-tri-tue-nhan-tao

