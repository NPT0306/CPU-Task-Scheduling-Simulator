
import hashlib

from django.contrib import messages
from django.shortcuts import redirect, render

from Schedule import Schedule

DEFAULT_QUANTUM = 2

SAMPLE_PROCESSES = [
    ("P1", 5, "USER", 0),
    ("P2", 3, "SYSTEM", 1),
    ("P3", 8, "USER", 0),
    ("P4", 2, "SYSTEM", 0),
]

_simulators = {}


def _get_simulator(session):
    if not session.session_key:
        session.save()
    key = session.session_key
    sim = _simulators.get(key)
    if sim is None:
        sim = Schedule(quantum=DEFAULT_QUANTUM)
        _simulators[key] = sim
    return sim


def _color_for(name):
    digest = hashlib.md5(name.encode('utf-8')).hexdigest()
    hue = int(digest, 16) % 360
    return f'hsl({hue}, 70%, 58%)'


def _build_context(request):
    sim = _get_simulator(request.session)
    rr_items = []
    node = sim.round_robin_queue.head
    while node is not None:
        rr_items.append(node.value)
        node = node.next
    pq_items = [entry[2] for entry in sorted(sim.priority_queue.heap)]
    for p in sim.process_storage:
        p.ui_color = _color_for(p.name)
    gantt_segments = []
    for i, name in enumerate(sim.gantt_history):
        if gantt_segments and gantt_segments[-1]['name'] == name:
            gantt_segments[-1]['end'] = i + 1
        else:
            gantt_segments.append({'name': name, 'start': i, 'end': i + 1})
    for seg in gantt_segments:
        seg['width'] = seg['end'] - seg['start']
        seg['color'] = _color_for(seg['name'])

    avg_turnaround, completion_ratio, total_time = sim.calculate_statistics()
    any_remaining = (not sim.priority_queue.is_empty()) or (not sim.round_robin_queue.is_empty())

    return {
        'quantum': sim.quantum,
        'clock': sim.clock,
        'rr_items': rr_items,
        'pq_items': pq_items,
        'processes': sim.process_storage,
        'gantt_segments': gantt_segments,
        'logs': list(reversed(sim.event_log)),
        'avg_turnaround': avg_turnaround,
        'completion_ratio': completion_ratio * 100,
        'total_time': total_time,
        'any_remaining': any_remaining,
        'has_processes': len(sim.process_storage) > 0,
        'sample_already_loaded': any(
            p.name in {row[0] for row in SAMPLE_PROCESSES} for p in sim.process_storage
        ),
    }


def index(request):
    return render(request, 'index.html', _build_context(request))


def set_quantum(request):
    if request.method == 'POST':
        sim = _get_simulator(request.session)
        raw = request.POST.get('quantum', '').strip()
        try:
            value = int(raw)
        except ValueError:
            messages.error(request, f'Quantum không hợp lệ: "{raw}". Hãy nhập một số nguyên.')
        else:
            if value < 1:
                messages.error(request, 'Quantum phải >= 1.')
            else:
                sim.set_quantum(value)
                sim.add_log(f'Set quantum = {value}')
                messages.success(request, f'Đã đặt Quantum = {value}.')
    return redirect('index')


def add_process(request):
    if request.method == 'POST':
        sim = _get_simulator(request.session)
        name = request.POST.get('name', '').strip()
        burst_raw = request.POST.get('burst_time', '').strip()
        process_type = request.POST.get('process_type', 'USER')
        priority_raw = request.POST.get('priority', '0').strip()

        try:
            burst_time = int(burst_raw)
        except ValueError:
            burst_time = -1
        try:
            priority = int(priority_raw)
        except ValueError:
            priority = 0

        if not name:
            messages.error(request, 'Tên process không được để trống.')
        elif burst_time <= 0:
            messages.error(request, 'Burst time phải là số nguyên > 0.')
        elif any(p.name == name for p in sim.process_storage):
            messages.error(request, f'Process "{name}" đã tồn tại, hãy chọn tên khác.')
        elif process_type not in ('USER', 'SYSTEM'):
            messages.error(request, 'Loại process không hợp lệ.')
        else:
            sim.add_process(name, burst_time, process_type, priority)
            queue_name = 'Priority Queue (heapq)' if process_type == 'SYSTEM' else 'Round Robin Queue (deque)'
            sim.add_log(f'Added {name} (type={process_type}, burst={burst_time}, priority={priority}) -> {queue_name}')
            messages.success(request, f'Đã thêm process "{name}" vào {queue_name}.')
    return redirect('index')


def load_sample(request):
    if request.method == 'POST':
        sim = _get_simulator(request.session)
        existing = {p.name for p in sim.process_storage}
        added = 0
        for name, burst, ptype, prio in SAMPLE_PROCESSES:
            if name not in existing:
                sim.add_process(name, burst, ptype, prio)
                added += 1
        if added:
            sim.add_log(f'Nạp {added} process mẫu (giống Main.py): P1..P4')
            messages.success(request, f'Đã nạp {added} process mẫu.')
        else:
            messages.info(request, 'Dữ liệu mẫu đã được nạp trước đó.')
    return redirect('index')


def step(request):
    if request.method == 'POST':
        sim = _get_simulator(request.session)
        if sim.priority_queue.is_empty() and sim.round_robin_queue.is_empty():
            messages.info(request, 'Không còn process nào trong queue để chạy.')
        else:
            before_clock = sim.clock
            sim.execute_step()
            if sim.gantt_history:
                ran_name = sim.gantt_history[-1]
                finished = next(
                    (p for p in sim.process_storage if p.name == ran_name and p.finish_time == before_clock),
                    None,
                )
                tail = f' — {ran_name} HOÀN THÀNH lúc t={before_clock}' if finished else ''
                ticks_ran = sim.clock - before_clock
                sim.add_log(f'[t={before_clock}->{sim.clock}] Chạy {ran_name} ({ticks_ran} tick){tail}')
            messages.success(request, 'Đã thực hiện 1 Step.')
    return redirect('index')


def run_all(request):
    if request.method == 'POST':
        sim = _get_simulator(request.session)
        if sim.priority_queue.is_empty() and sim.round_robin_queue.is_empty():
            messages.info(request, 'Không còn process nào trong queue để chạy.')
        else:
            sim.add_log(f'Run All: bắt đầu từ t={sim.clock}')
            sim.run_all()
            sim.add_log(f'Run All: hoàn tất, clock={sim.clock}')
            messages.success(request, 'Đã chạy Run All đến khi hết process.')
    return redirect('index')


def reset(request):
    if request.method == 'POST':
        sim = _get_simulator(request.session)
        sim.reset_simulation()
        messages.success(request, 'Đã reset: xoá queues, log, Gantt data, clock = 0 (giữ nguyên Quantum).')
    return redirect('index')
