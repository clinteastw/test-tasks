def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']
   
    lesson_sec = set(range(lesson[0], lesson[1]))
    pupils_sec = set()
    tutors_sec = set()
    
    for i in range(1, len(pupil), 2):
        pupils_sec.update(range(pupil[i-1], pupil[i]))
         
    for i in range(1, len(tutor), 2):
        tutors_sec.update(range(tutor[i-1], tutor[i]))
   
    return len(lesson_sec & pupils_sec & tutors_sec)


