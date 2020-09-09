import pandas as pd

def get_bid_url(bidno, bidseq):
    """입찰공고번호와 차수로 입찰공고 상세페이지 url을 만듭니다."""
    url = "http://www.g2b.go.kr:8081/ep/invitation/publish/bidInfoDtl.do"
    url = f"{url}?bidno={bidno}&bidseq={bidseq}&releaseYn=Y&taskClCd=5"
    return url


def parse_table(table_data):
    """
    컬럼이 4개인 table 태그에서 컬럼-값 형태로 전처리를 해서 반환합니다.
    컬럼이 3개보다 작으면 입력값을 전처리 후 반환합니다.
    """
    
    col_count = table_data.shape[1]
    if  col_count % 2 == 1:
        return
    
    if col_count < 3 :
        table_data.columns = ["컬럼명", "내용"]
        table_data = table_data[table_data["컬럼명"] != table_data["내용"]]
        table_data = table_data.set_index("컬럼명")
        return table_data
        
    desc_01 = table_data.iloc[:, [0, 1]]
    desc_02 = table_data.iloc[:, [2, 3]]
    # concat을 위해 컬럼명을 desc_01과 같도록 만듭니다.
    desc_01.columns = ["컬럼명", "내용"]
    desc_02.columns = ["컬럼명", "내용"]
    # 전처리한 데이터를 붙여줍니다.
    desc = pd.concat([desc_01, desc_02])
    # colspan 으로 합쳐진 데이터에는 같은 내용이 들어가 있습니다. 이 데이터는 제외합니다.
    # 컬럼명과 내용이 다른 데이터만 사용합니다.
    desc = desc[desc["컬럼명"] != desc["내용"]]
    # 데이터가 모두 결측치라면 제거합니다.
    desc = desc.dropna(how="all")
    # 컬럼명을 인덱스로 설정합니다.
    desc = desc.set_index("컬럼명")
    # 처리가 끝난 desc 값을 반환합니다.
    return desc


def get_bid_info(bidno, bidseq):
    """상세페이지 정보를 가져옵니다. 내부에서 get_bid_url, parse_table 을 호출합니다."""
    url = get_bid_url(bidno, bidseq)

    try:
        table = pd.read_html(url)
        desc_list = []
        for table_no in range(1, 6):
            table_result = parse_table(table[table_no])
            desc_list.append(table_result)

        return pd.concat(desc_list)
    except:
        return False
