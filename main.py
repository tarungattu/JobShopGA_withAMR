from JobShopScheduler import JobShopScheduler
import benchmarks
import distances

def main():
    machine_data = benchmarks.ft06['machine_data']
    ptime_data = benchmarks.ft06['ptime_data']
    machine_data4 = benchmarks.pinedo['machine_data']
    ptime_data4 = benchmarks.pinedo['ptime_data']
    machine_data6 = benchmarks.ft06['machine_data']
    ptime_data6 = benchmarks.ft06['ptime_data']
    machine_data5  = benchmarks.la01['machine_data']
    ptime_data5  = benchmarks.la01['ptime_data']
    machine_data10 = benchmarks.la01['machine_data']
    ptime_data10 = benchmarks.la01['ptime_data']
    
    
    
    scheduler1 = JobShopScheduler(5, 10, 3, 350, 0.7, 0.5, 450, machine_data5, ptime_data5)    
    print(scheduler1.operation_data)
    # scheduler1.set_distance_matrix(distances.four_machine_matrix)
    scheduler1.set_distance_matrix(distances.five_machine_matrix)
    
    scheduler1.display_schedule = 1
    scheduler1.display_convergence = 1
    scheduler1.enable_travel_time = 1
    chromosome1 = scheduler1.GeneticAlgorithm()
    
    # scheduler1.reschedule(2, 3)
    # chromosome2 = scheduler1.GeneticAlgorithm()
    
    print('AMR MACHINE SEQUENCES')
    print(chromosome1.amr_machine_sequences)
    print(chromosome1.amr_ptime_sequences)
    # print(chromosome2.amr_machine_sequences)
    # print(chromosome2.amr_ptime_sequences)
    
    
if __name__ == '__main__':
    main()