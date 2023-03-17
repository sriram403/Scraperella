from CUKU.components import details_collector as dc

name_to_search = "Priyanka Mohan"
details_needed_amount = 10
run_in_backend = True

def start_the_cuku():
    dc.RUN(name_to_search,details_needed_amount,run_in_backend)

if __name__ == "__main__":
    start_the_cuku()
