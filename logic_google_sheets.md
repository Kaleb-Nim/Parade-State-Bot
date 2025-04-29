# Logic for processing parade_state google sheet

The "Name" column of the 24 hard coded rows directly coorespond to the 24 name from the final telegram message, the order doesn't change, use this to simplify the logic, no need to name match "Sch comd --> Pang Kee Hwee"
"1" in the googlesheets represents "Present"/P in the final message
For status other then LL,HL,OIL Location is needed represented by the @xx E.g OB @PLAB

Other mapping cases from google sheets --> Final message
"DS OFF" --> OIL (DS OFF)
"DO Off" --> OIL (DO OFF)
"OFF" --> OIL

Example columns and rows
```
Mon		Tue		Wed		Thu		Fri			
28/04/2025		29/04/2025		30/04/2025		01/05/2025		02/05/2025			
AM	PM	AM	PM	AM	PM	AM	PM	AM	PM		
1	1	1	1	1	1	PH	PH				
OML	OML					PH	PH				
						PH	PH				
LL	LL	1	1	1	1	PH	PH	1	1		
CSE	CSE	CSE	CSE	CSE	CSE	PH	PH	CSE	CSE		
CPE	CPE	CPE	CPE	CPE	CPE	PH	PH	1	1		
OL	OL	OL	OL	OL	OL	PH	PH	OL	OL		
HL	HL	HL	HL	HL	HL	HL	HL	HL	HL	HL	HL
						PH	PH				
1	1	WFH	WFH	OB-LVS	1	PH	PH	1	1		
						PH	PH				
1	1	1	1	1	1	PH	PH	1	1		
						PH	PH				
						PH	PH				
1	1	1	1	1	1	PH	PH	1	1		
1	1	1	1	1	1	PH	PH	1	1		
1	1	1	1	1	1	PH	PH	1	1		
OL	OL	OL	OL	1	1	PH	PH	1	1		
1	1	1	1	1	1	PH	PH	1	1		
LL	LL	1	1	1	1	PH	PH	LL	LL		
1	1	1	1	1	1	PH	PH	1	1		
1	1	1	1	1	1	PH	PH	1	1		
1	1	1	1	1	1	PH	PH	1	1		
						PH	PH				
1	1	1	1	1	1	PH	PH	1	1		
						PH	PH	L/L	L/L		
						PH	PH				
						PH	PH				
											
DS OFF	DS OFF	1	1	MA @ SGH	1	OL @ CHINA	OL @ CHINA	OL @ CHINA	OL @ KOREA	OL @ KOREA	OL @ KOREA
1	1	1	1	1	1	PH	PH	1	1		
1	1	1	1	1	1	PH	PH	1	1		
```
Each day is represented by 2 columns, AM and PM, with the date and the day being a merge cell of size 2 between the AM and PM

The A column stores all the names

```
29/04/2025
Name

Tan Pau Siang
Pang Kee Hwee
Chua Seong Bee
Andrew Kwek 
Tay Chin Choon
Kok Wai Chung
Edwin Tan
Jeffrey Kor
Or Ling Wan
Michael Ng
Marcus Soh
Tan Toh Choon
Ng Boon Hwee
Leonard Tan
Brandon Lim
Gin Tay
Wilfred Hu
Edmund Cheong
Jonathan Koe
Benson Ong
Edmund Yeo
Tan Thian Kiong
Tan Kok Kuan
Derrick Tan
Tay Bijun
Magendran S/O Raju
Tan Eng Chuan
Ignatios Quek
Edwin Ngow
Benjamin Yeo
Chen Yiming
Sherwyn Sim
Kaleb Nim
Notes
```