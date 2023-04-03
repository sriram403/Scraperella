from CUKU.components import details_collector as dc

name_to_search = "Chandler bing Joey"
details_needed_amount = 2
run_in_backend = True

def start_the_cuku():
    dc.RUN(name_to_search,details_needed_amount,run_in_backend)

if __name__ == "__main__":
    start_the_cuku()
