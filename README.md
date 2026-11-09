\# Apache Arrow DataFusion – Paper Reproduction



\*\*Advanced Database Systems – Team 9\*\*



\## 1. Giới thiệu



Đồ án tái hiện và đánh giá bài báo:



Andrew Lamb et al. (2024), \*Apache Arrow DataFusion: A Fast, Embeddable, Modular Analytic Query Engine\*, SIGMOD-Companion '24.



DOI: https://doi.org/10.1145/3626246.3653368



Mục tiêu là tìm hiểu kiến trúc DataFusion, các cơ chế tối ưu truy vấn, thực thi song song và khả năng mở rộng; đồng thời tái hiện một số thực nghiệm so sánh DataFusion với DuckDB.



\## 2. Nội dung thực hiện



\- Tái hiện benchmark TPC-H SF=10 với 22 truy vấn.

\- Tái hiện benchmark ClickBench với 43 truy vấn.

\- Tái hiện benchmark H2O-G với 10 truy vấn.

\- Phân tích kế hoạch thực thi truy vấn bằng EXPLAIN.

\- Thử nghiệm scalability với 1, 2, 4, 8 và 14 logical processors.

\- Phát triển scalar UDF `price\_band` để minh họa khả năng mở rộng của DataFusion.



\## 3. Môi trường thực nghiệm



\- Hệ điều hành: Windows 11

\- CPU: Intel Core Ultra 5 235U

\- RAM: 15.4 GB

\- Apache DataFusion: 32.0.0

\- DuckDB: 0.9.1

\- PyArrow: 25.0.1



\## 4. Kết quả thực nghiệm



\- TPC-H: DataFusion nhanh hơn ở 9/22 truy vấn.

\- ClickBench: DataFusion chạy thành công 41/43 truy vấn; Q34 và Q35 không có kết quả do lỗi thực thi.

\- H2O-G: DataFusion nhanh hơn ở 7/10 truy vấn.

\- Scalability: trên phép thử H2O-G Q1, DataFusion đạt thời gian tốt nhất tại 8 logical processors trong các mức đã khảo sát.



Các kết quả được đo trên máy local, không phải số liệu gốc của bài báo.



\## 5. Cấu trúc mã nguồn và dữ liệu



Repository được tổ chức như sau:



\- `tpch/`: Script Python và các file SQL để chạy benchmark TPC-H SF=10.

\- `clickbench/`: Script Python và các file SQL để chạy benchmark ClickBench.

\- `h2o/`: Script Python và các file SQL để chạy benchmark H2O-G.

\- `common/`: Các script hỗ trợ thực thi truy vấn trên DataFusion và DuckDB.

\- `src/`: Các script chuyển đổi dữ liệu, triển khai UDF và mã nguồn thực nghiệm.

\- `results/tpch/`: Kết quả TPC-H dưới dạng CSV.

\- `results/clickbench/`: Kết quả ClickBench dưới dạng CSV.

\- `results/h2o/`: Kết quả H2O-G dưới dạng CSV.

\- `results/scalability/`: Kết quả thử nghiệm khả năng mở rộng theo số luồng xử lý.

\- `requirements.txt`: Danh sách thư viện Python và phiên bản sử dụng.



Các dataset dung lượng lớn không được đưa lên GitHub.

Người chạy cần chuẩn bị dữ liệu theo hướng dẫn tại Mục 6.



Các file CSV trong `results/` là kết quả thực nghiệm

được nhóm thu thập trên môi trường Windows 11.



\## 6. Hướng dẫn tái lập thí nghiệm



\### 6.1. Cài đặt môi trường



Các thực nghiệm của nhóm được thực hiện trên môi trường:



\- Hệ điều hành: Windows 11

\- Apache DataFusion: 32.0.0

\- DuckDB: 0.9.1

\- PyArrow: 25.0.1

\- psutil: 7.2.2



Máy chạy cần cài đặt Python và Git.



Sau khi tải repository từ GitHub, mở CMD tại thư mục gốc của project và thực hiện:



```cmd

python -m venv .venv

.venv\\Scripts\\python.exe -m pip install -r requirements.txt

```



Các phiên bản thư viện được khai báo trong file `requirements.txt`, tương ứng với môi trường thực nghiệm của nhóm.



Lưu ý: Khả năng cài đặt thành công còn phụ thuộc vào phiên bản Python và tính tương thích của các thư viện.



\### 6.2. Chuẩn bị dữ liệu



Do dung lượng lớn, các bộ dữ liệu benchmark không được đưa trực tiếp lên GitHub. Người chạy cần chuẩn bị dữ liệu theo đúng cấu trúc và đường dẫn được khai báo trong các file SQL.



\*\*a. TPC-H SF=10\*\*



Chuẩn bị bộ dữ liệu TPC-H ở scale factor 10 dưới định dạng Parquet và đặt trong thư mục `tpch/tpch\_dataset/`.



Cấu trúc dữ liệu yêu cầu:



```text

tpch/

└── tpch\_dataset/

&#x20;   ├── customer/

&#x20;   │   └── part-0.parquet

&#x20;   ├── orders/

&#x20;   │   └── part-0.parquet

&#x20;   ├── lineitem/

&#x20;   │   └── part-0.parquet

&#x20;   ├── part/

&#x20;   │   └── part-0.parquet

&#x20;   ├── partsupp/

&#x20;   │   └── part-0.parquet

&#x20;   ├── region/

&#x20;   │   └── part-0.parquet

&#x20;   ├── supplier/

&#x20;   │   └── part-0.parquet

&#x20;   └── nation/

&#x20;       └── part-0.parquet

```



Hai engine sử dụng cùng các file Parquet:



\- DataFusion đọc dữ liệu thông qua `CREATE EXTERNAL TABLE`.

\- DuckDB tạo các view sử dụng hàm `read\_parquet()`.



Các cấu hình được lưu tại:



\- `tpch/create-win-datafusion.sql`

\- `tpch/create-win-duckdb.sql`



Repository có script `src/convert\_tpch\_sf10.py` được nhóm sử dụng trong quá trình chuẩn bị dữ liệu. Quy trình tự động tạo lại toàn bộ dataset TPC-H SF=10 chưa được tích hợp thành một lệnh duy nhất.



\*\*b. ClickBench\*\*



Chuẩn bị dữ liệu ClickBench dưới định dạng Parquet, đặt trong thư mục:



```text

clickbench/

└── hits\_multi/

&#x20;   ├── hits\_\*.parquet

&#x20;   └── ...

```



DataFusion tạo bảng ngoài `hits` từ thư mục `hits\_multi`, trong khi DuckDB tạo view từ các file `hits\_\*.parquet`.



Trong cấu hình DuckDB, các cột `EventTime` và `EventDate` được chuyển đổi kiểu dữ liệu khi tạo view.



Các cấu hình được lưu tại:



\- `clickbench/create-multi-datafusion.sql`

\- `clickbench/create-multi-duckdb.sql`



\*\*c. H2O-G\*\*



Chuẩn bị file dữ liệu CSV có tên:



`G1\_1e7\_1e2\_5\_0.csv`



Đặt file trực tiếp trong thư mục `h2o/`:



```text

h2o/

├── G1\_1e7\_1e2\_5\_0.csv

├── create-single-datafusion.sql

├── create-single-duckdb.sql

└── run\_h2o\_windows.py

```



DataFusion đọc dữ liệu CSV thông qua bảng ngoài với kiểu dữ liệu được khai báo tường minh.



DuckDB sử dụng hàm `read\_csv\_auto()` để đọc cùng file CSV và tự nhận diện kiểu dữ liệu.



Các cấu hình được lưu tại:



\- `h2o/create-single-datafusion.sql`

\- `h2o/create-single-duckdb.sql`



\### 6.3. Chạy các benchmark



Sau khi cài đặt môi trường và chuẩn bị đầy đủ dữ liệu, mở CMD trên Windows.



Các lệnh dưới đây giả định người dùng đã đứng tại thư mục gốc của repository.



\*\*a. Chạy TPC-H\*\*



```cmd

cd tpch

..\\.venv\\Scripts\\python.exe run\_tpch\_windows.py

```



Script thực hiện 22 truy vấn TPC-H trên DataFusion và DuckDB.



Sau khi hoàn thành, script tạo các file kết quả CSV và sao chép chúng vào `results/latest/`.



\*\*b. Chạy ClickBench\*\*



Quay lại thư mục gốc repository, sau đó chạy:



```cmd

cd clickbench

..\\.venv\\Scripts\\python.exe run\_clickbench\_windows.py

```



Script được thiết kế để thực hiện 43 truy vấn ClickBench trên hai engine.



Trong thực nghiệm của nhóm:



\- DuckDB thực thi thành công 43/43 truy vấn.

\- DataFusion thực thi thành công 41/43 truy vấn.

\- Hai truy vấn Q34 và Q35 gặp lỗi thực thi trên DataFusion.



Lưu ý: Script hiện tại sử dụng `check=True` khi gọi tiến trình con. Vì vậy, nếu một truy vấn gặp lỗi, quá trình benchmark có thể dừng ngay và không chạy hết các truy vấn còn lại.



Các file kết quả đã thu thập được trong quá trình thực nghiệm được lưu riêng tại `results/clickbench/`.



\*\*c. Chạy H2O-G\*\*



Quay lại thư mục gốc repository, sau đó chạy:



```cmd

cd h2o

..\\.venv\\Scripts\\python.exe run\_h2o\_windows.py

```



Script thực hiện 10 truy vấn H2O-G trên DataFusion và DuckDB.



Các file kết quả được tạo trong thư mục chạy:



\- `h2o\_datafusion.csv`

\- `h2o\_duckdb.csv`



Kết quả thực nghiệm mà nhóm đã thu thập được lưu tại `results/h2o/`.



\### 6.4. Phương pháp đo thời gian



Các script benchmark sử dụng `timeit.default\_timer()` để đo thời gian thực thi truy vấn.



Đối với mỗi truy vấn:



1\. Chạy truy vấn 5 lần.

2\. Không lưu kết quả thời gian của 2 lần chạy đầu.

3\. Lưu thời gian thực thi của 3 lần chạy cuối.

4\. Xuất kết quả dưới định dạng CSV để phục vụ phân tích và so sánh.



Trong các script benchmark hiện tại:



\- DataFusion sử dụng `target\_partitions=1`.

\- DuckDB sử dụng `PRAGMA threads=1`.



Hai tham số này điều khiển cách thực thi của từng engine nhưng không nhất thiết tạo ra mức sử dụng tài nguyên hoàn toàn tương đương.



\### 6.5. Kết quả thực nghiệm



Các kết quả đã thu thập được lưu trong thư mục `results/`:



\- `results/tpch/`: Kết quả TPC-H SF=10.

\- `results/clickbench/`: Kết quả ClickBench.

\- `results/h2o/`: Kết quả H2O-G.

\- `results/scalability/`: Kết quả thử nghiệm thay đổi số logical processors.



Các kết quả này được đo trên máy tính của nhóm, không phải số liệu gốc được công bố trong bài báo.



Kết quả thực nghiệm có thể thay đổi tùy theo phần cứng, môi trường phần mềm, cấu hình thực thi và dữ liệu đầu vào.



\### 6.6. Giới hạn tái lập



Repository cung cấp mã nguồn benchmark, cấu hình SQL, các thư viện phụ thuộc và kết quả thực nghiệm đã thu thập.



Tuy nhiên, cần lưu ý:



\- Các dataset lớn không được lưu trực tiếp trong repository.

\- Quy trình tải và tạo lại toàn bộ dataset chưa được tự động hóa hoàn chỉnh.

\- Một số truy vấn ClickBench trên DataFusion gặp lỗi thực thi trong môi trường của nhóm.

\- Kết quả scalability được lưu dưới dạng CSV; quy trình thực thi tương ứng chưa được đóng gói đầy đủ thành một script chạy tự động trong repository.

\- Các script benchmark có thể xóa hoặc ghi lại file CSV kết quả cũ trong thư mục thực thi. Người dùng nên sao lưu dữ liệu kết quả trước khi chạy lại.



Do đó, repository hỗ trợ nghiên cứu, kiểm tra mã nguồn và tái lập các thực nghiệm khi đã chuẩn bị đúng dữ liệu và môi trường, nhưng chưa phải một hệ thống benchmark hoàn toàn tự động.





\## 7. Nguồn tham khảo và đóng góp của nhóm



\### 7.1. Tài liệu tham khảo



1\. Andrew Lamb et al. (2024). \*Apache Arrow DataFusion: A Fast, Embeddable, Modular Analytic Query Engine\*. SIGMOD-Companion '24. https://doi.org/10.1145/3626246.3653368



2\. Repository benchmark tham khảo: https://github.com/JayjeetAtGithub/datafusion-duckdb-benchmark



\### 7.2. Mã nguồn tham khảo



Nhóm sử dụng repository benchmark nêu trên làm cơ sở để nghiên cứu và tái hiện các phép thử TPC-H, ClickBench và H2O-G.



Các script hỗ trợ trong thư mục `common/` và những file cấu hình, truy vấn benchmark được kế thừa hoặc điều chỉnh từ mã nguồn tham khảo.



\### 7.3. Phần triển khai và điều chỉnh của nhóm



Trong quá trình thực nghiệm, nhóm thực hiện các công việc:



\- Thiết lập môi trường chạy DataFusion và DuckDB trên Windows 11.

\- Xây dựng hoặc điều chỉnh các script `run\_\*\_windows.py` để thực hiện benchmark trong môi trường của nhóm.

\- Chuẩn bị và chuyển đổi dữ liệu TPC-H SF=10 sang định dạng Parquet.

\- Thực hiện các phép đo hiệu năng và tổng hợp kết quả vào thư mục `results/`.

\- Thử nghiệm khả năng mở rộng theo số logical processors.

\- Triển khai scalar UDF `price\_band` để khảo sát khả năng mở rộng chức năng của DataFusion.

\- Phân tích kết quả thực nghiệm và đối chiếu với các nội dung được trình bày trong bài báo.



Những thay đổi và kết quả thực nghiệm của nhóm không được xem là mã nguồn hoặc số liệu chính thức của các tác giả bài báo.



Khi sử dụng hoặc phân phối lại mã nguồn kế thừa, cần tuân thủ điều khoản giấy phép của repository gốc.



