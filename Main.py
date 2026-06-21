from Schedule import Schedule


def main():
    scheduler = Schedule(quantum=2)

    # Thêm vài process SYSTEM (chạy theo Priority Queue) và USER (Round Robin)
    scheduler.add_process("P1", burst_time=5, process_type="USER", priority=0)
    scheduler.add_process("P2", burst_time=3, process_type="SYSTEM", priority=1)
    scheduler.add_process("P3", burst_time=8, process_type="USER", priority=0)
    scheduler.add_process("P4", burst_time=2, process_type="SYSTEM", priority=0)

    scheduler.run_all()

    print("Gantt chart:", " -> ".join(scheduler.render_gantt_chart()))

    avg_turnaround, completion_ratio, total_time = scheduler.calculate_statistics()
    print(f"Average turnaround time: {avg_turnaround:.2f}")
    print(f"Completion ratio: {completion_ratio:.2%}")
    print(f"Total simulation time (clock): {total_time}")

    print("\nChi tiết từng process:")
    for p in scheduler.process_storage:
        print(f"  {p.name}: arrival={p.arrival_time}, finish={p.finish_time}, "
              f"turnaround={p.turnaround_time}, completed={p.completed}")


if __name__ == "__main__":
    main()