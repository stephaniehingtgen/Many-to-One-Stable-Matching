import queue

debug = False
studentPref = {
    "ally":     ["mayo", "hopkins", "iowa", "slc"],
    "bob":      ["hopkins", "iowa", "slc", "mayo"],
    "caroline": ["iowa", "slc", "mayo", "hopkins"],
    "david":    ["iowa", "hopkins", "slc", "mayo"],
    "emma":     ["iowa", "hopkins", "mayo", "slc"],
    "freddy":   ["hopkins", "mayo", "iowa", "slc"],
    "greg":     ["mayo", "hopkins", "iowa", "slc"],
    "hannah":   ["iowa", "mayo", "hopkins", "slc"]
}
hospitalPref = {
    "mayo":     ["bob", "caroline", "david", "ally", "hannah", "greg", "emma", "freddy"],
    "hopkins":  ["emma", "greg", "freddy", "caroline", "ally", "bob", "david", "hannah"],
    "iowa":     ["bob", "david", "ally", "caroline", "emma", "hannah", "freddy", "greg"],
    "slc":      ["freddy", "greg", "hannah", "emma", "david", "ally", "bob", "caroline"]
}
jobsPerHospitals = {
    "mayo": 1,
    "hopkins": 2,
    "iowa": 1,
    "slc": 2
}
# m hospitals, each with a certain number of available positions for hiring residents. 
# n medical students graduating in a given year, each interested in joining one of the hospitals
# Each hospital had a ranking of the students in order of preference, and each student had a ranking of the hospitals in order of preference. 
# We will assume that there were more students graduating than there were slots available in the m hospitals.

def main():
    students = studentPref.keys()
    hospitals = hospitalPref.keys()
    pointerCounter = {}
    studentPrefDict = {}
    studentEmployeeDict = {}
    openJobs = queue.Queue()

    for i in range(len(hospitals)):
        # put all the free students in a queue
        for j in range(jobsPerHospitals[hospitals[i]]):
            openJobs.put(hospitals[i])
        pointerCounter[hospitals[i]] = 0
    for i in range(len(students)):
        # Not given employees yet
        studentEmployeeDict[students[i]] = None
        # Make dictionary to easy get if preference
        studentPrefDict[students[i]] = {}
        for j in range(len(hospitals)):
            # Save in a dictornary an array for every student that maps the hospital name to the preference position they are in
            studentPrefDict[students[i]][studentPref[students[i]][j]] = j
    # Loop through students who aren't matched yet
    while not openJobs.empty():
        job = openJobs.get()
        # Get the next up preference for the student
        hospitalPreference = hospitalPref[job][pointerCounter[job]]
        pointerCounter[job] = pointerCounter[job] + 1
        # Has the hospital already given the job away?
        taken = studentEmployeeDict[hospitalPreference]
        if taken != None:
            # Does the hospital prefer this student?
            currentPosition = studentPrefDict[hospitalPreference][taken]
            proposingPosition = studentPrefDict[hospitalPreference][job]
            if currentPosition > proposingPosition:
                # The current student is more preferred by the hospital, switch the students out
                openJobs.put(taken)
                if debug:
                    print("Matching %s with %s. Removing %s" % (job, hospitalPreference, taken))
                studentEmployeeDict[hospitalPreference] = job
            else:
                if debug:
                    print("No match yet for %s" % (job))
                # The current student isn't more preferred, push back onto the queue
                openJobs.put(job)
        else:
            if debug:
                print("Matching %s with %s" % (job, hospitalPreference))
            # Not yet taken - match them for now
            studentEmployeeDict[hospitalPreference] = job
    print("MATCHING FOUND: ")
    print(studentEmployeeDict)

if __name__ == "__main__":
    main()