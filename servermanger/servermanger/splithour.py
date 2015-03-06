__author__ = 'Administrator'
def splithour(hour):
    checktime = []
    if hour== all:
        for check in range(0,24):
            checktime.append(str(check))
        print checktime
    elif ','  not in str(hour):
        isfind = hour.find('-')
        if isfind == 1:
            aa = hour.split('-')
            start = aa[0]
            end = aa[1]
            print start,end
            for check in range(int(start),int(end)+1):
                if len(str(check)) == 1:
                    check = ('0' + str(check))
		checktime.append(str(check))
	else:
	    checktime.append(hour)
    else:
        checktime1 = hour.split(',')

        for value in checktime1:

            isfind = value.find('-')
            if isfind == -1:
                pass
            else:
                aa = value.split('-')
                start = aa[0]
                end = aa[1]

                for check in range(int(start),int(end)+1):
                    if len(str(check)) == 1:
                        check = ('0' + str(check))
		    checktime.append(str(check))
        for length in range(1,len(checktime1)):

            checktime.append(checktime1[length])
        print checktime
    return checktime


