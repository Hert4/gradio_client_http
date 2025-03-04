### This file use only for created a fakedb for testing purpose

import duckdb


conn = duckdb.connect("./data/fakedb.db")

# init all here
conn.execute(
    """\
-- Tạo bảng trong DuckDB
CREATE TABLE gmes_production_report (
    Model TEXT,
    Process TEXT,
    Total_Yield FLOAT,
    Total_OK INTEGER,
    Total_NG INTEGER,
    Total INTEGER,
    Yield_2024_02_12 FLOAT,
    Yield_2024_02_13 FLOAT,
    Yield_2024_02_14 FLOAT
);

-- Chèn dữ liệu giả
INSERT INTO gmes_production_report (Model, Process, Total_Yield, Total_OK, Total_NG, Total, Yield_2024_02_12, Yield_2024_02_13, Yield_2024_02_14) VALUES
('Model A', 'Process 1', 98.5, 500, 10, 510, 98.2, 98.6, 98.4),
('Model B', 'Process 2', 97.2, 480, 14, 494, 97.0, 97.3, 97.1),
('Model C', 'Process 3', 99.0, 600, 6, 606, 99.1, 99.0, 98.9),
('Model D', 'Process 1', 96.8, 450, 20, 470, 96.5, 96.7, 96.9),
('Model E', 'Process 2', 95.5, 420, 22, 442, 95.4, 95.6, 95.3),
('Model F', 'Process 3', 98.0, 510, 10, 520, 97.8, 98.1, 98.2),
('Model G', 'Process 1', 99.2, 630, 5, 635, 99.0, 99.3, 99.1),
('Model H', 'Process 2', 97.6, 470, 12, 482, 97.5, 97.7, 97.4),
('Model I', 'Process 3', 98.9, 590, 7, 597, 98.7, 98.8, 99.0),
('Model J', 'Process 1', 97.3, 490, 15, 505, 97.1, 97.4, 97.2),
('Model K', 'Process 2', 96.0, 440, 18, 458, 95.8, 96.1, 95.9),
('Model L', 'Process 3', 98.3, 520, 9, 529, 98.2, 98.4, 98.1),
('Model M', 'Process 1', 99.1, 625, 6, 631, 99.0, 99.2, 98.9),
('Model N', 'Process 2', 97.9, 485, 11, 496, 97.8, 98.0, 97.7),
('Model O', 'Process 3', 98.6, 580, 8, 588, 98.5, 98.7, 98.4),
('Model P', 'Process 1', 96.7, 445, 19, 464, 96.6, 96.8, 96.5),
('Model Q', 'Process 2', 95.8, 430, 23, 453, 95.7, 95.9, 95.6),
('Model R', 'Process 3', 97.4, 495, 14, 509, 97.3, 97.5, 97.2),
('Model S', 'Process 1', 98.8, 600, 7, 607, 98.7, 98.9, 98.6),
('Model T', 'Process 2', 97.1, 475, 13, 488, 97.0, 97.2, 97.3);

-- Tạo bảng Table Worst
CREATE TABLE table_worst (
    Model TEXT,
    Process TEXT,
    Error_Name TEXT,
    Error_Count INTEGER,
    Error_Percentage FLOAT
);

-- Chèn dữ liệu giả vào Table Worst
INSERT INTO table_worst (Model, Process, Error_Name, Error_Count, Error_Percentage) VALUES
('Model A', 'Process 1', 'Defect A', 5, 1.0),
('Model B', 'Process 2', 'Defect B', 8, 1.6),
('Model C', 'Process 3', 'Defect C', 3, 0.5),
('Model D', 'Process 1', 'Defect D', 10, 2.1),
('Model E', 'Process 2', 'Defect E', 12, 2.7),
('Model F', 'Process 3', 'Defect F', 7, 1.3),
('Model G', 'Process 1', 'Defect G', 4, 0.8),
('Model H', 'Process 2', 'Defect H', 6, 1.2),
('Model I', 'Process 3', 'Defect I', 5, 1.0),
('Model J', 'Process 1', 'Defect J', 9, 1.8);
"""
)
