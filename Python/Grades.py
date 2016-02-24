def print_grades(grades):
    
    for grade in grades:
        print grade

def grades_sum(scores):
    total = 0
    for score in scores:
        total += score
    return total

print grades_sum(grades)

def grades_average(grades):
    return grades_sum(grades) / float(len(grades))

print grades_average(grades)

def grades_variance(scores):
    average = grades_average(scores)
    variance = 0
    for score in scores:
        variance += (average - score) ** 2
    return variance / float(len(grades))

def grades_std_deviation(variance):
    return variance ** 0.5

variance = grades_variance(grades)
print grades_std_deviation(variance)
