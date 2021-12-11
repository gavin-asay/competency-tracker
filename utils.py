from os import system, name
from re import split as resplit, fullmatch


def getlongest(sqlresults):
    # used to set column width for each column in sql results
    longest_len = [0] * len(sqlresults[0])
    for result in sqlresults:
        for i, column in enumerate(result):
            length = len(str(column))
            if length > longest_len[i]:
                longest_len[i] = length

    for i, leng in enumerate(longest_len):
        longest_len[i] = leng + 3
    return longest_len


def clear_console():
    system('cls' if name in ('nt', 'dos') else 'clear')


def paginate_list(sqlresults, table):
    pages = [[]]
    pagesindex = 0
    for result in sqlresults:
        pages[pagesindex].append(result)

        if len(pages[pagesindex]) == 20:
            pages.append([])
            pagesindex += 1

    global currentpage
    currentpage = 0
    global pagecount
    pagecount = pagesindex + 1

    def printpage():
        global currentpage
        global pagecount
        column_widths = getlongest(pages[currentpage])
        clear_console()
        print(pages[currentpage])

        while True:
            print(f'Page {currentpage + 1} of {pagecount}')

            if table == 'Users':
                print(
                    f'{"User ID":<{max(column_widths[0], 10)}}{"First Name":<{max(column_widths[1], 13)}}{"Last Name":<{max(column_widths[2], 12)}}{"Phone":<{column_widths[3]}}{"Email":<{column_widths[4]}}{"Hire Date":<{max(column_widths[5], 12)}}{"Manager":<10}{"Active":<9}')
                for result in pages[currentpage]:
                    print(f'{result[0]:<{max(column_widths[0], 10)}}{result[1]:<{column_widths[1]}}{result[2]:<{column_widths[2]}}{result[3]:<{column_widths[3]}}{result[4]:<{column_widths[4]}}{result[5]:<{max(column_widths[5], 12)}}{result[6]:<10}{result[7]:<9}')
            elif table == 'Competencies':
                print(
                    f'{"Competency ID":<{max(column_widths[0], 16)}}{"Name":<{column_widths[1]}}{"Date Created":<{max(column_widths[2], 15)}}{"Active":<9}')
                for result in pages[currentpage]:
                    print(
                        f'{result[0]:<{max(column_widths[0], 16)}}{result[1]:<{column_widths[1]}} {result[2]:<{max(column_widths[2], 15)}} {result[3]:<9}')
            elif table == 'Assessments':
                print(
                    f'{"Assessment ID":<{max(column_widths[0], 16)}}{"Competency":<{max(column_widths[1], 13)}}{"Name":<{column_widths[2]}}{"Date Created":<{max(column_widths[3], 15)}}{"Active":<9}')
                for result in pages[currentpage]:
                    print(
                        f'{result[0]:<{max(column_widths[0], 16)}}{result[1]:<{max(column_widths[1], 13)}}{result[2]:<{column_widths[2]}}{result[3]:<{max(column_widths[3], 15)}}{result[4]:<9}')
            elif table == 'Results':
                print(
                    f'{"Result ID":<{max(column_widths[0], 12)}}{"Assessment":<{column_widths[1]}}{"User":<{column_widths[2]}}{"Score":<8}{"Date Taken":<{max(column_widths[3], 13)}}{"Active":<9}')
                for result in pages[currentpage]:
                    print(
                        f'{result[0]:<{max(column_widths[0], 12)}}{result[1]:<{column_widths[1]}}{result[2]:<{column_widths[2]}}{result[3]:<{max(column_widths[3], 13)}}{result[4]:<9}')

            selection = input(
                f'\n{"Enter N for next page, P for previous, or a page number, enter X to exit." if pagecount > 1 else "Enter X to exit."} To view and edit an individual user\'s data, enter # then the user ID. (Example #29): ')
            if selection.upper() in ['N', 'P', *[str(num) for num in range(1, len(pages) + 1)]]:
                if selection.upper() == 'N' and currentpage + 1 < len(pages):
                    currentpage += 1
                    printpage()
                elif selection.upper() == 'N' and currentpage + 1 > 1:
                    currentpage -= 1
                    printpage()
                elif int(selection) in range(1, len(pages)):
                    currentpage = int(selection) - 1
                    printpage()
            elif selection.upper() == 'X':
                break
            elif fullmatch(r'#\d+', selection):
                return int(resplit(r'#', selection, 1)[1])

    lookupcheck = printpage()
    if isinstance(lookupcheck, int):
        return lookupcheck


def paginate_list_forlookup(sqlresults, table):
    pages = [[]]
    pagesindex = 0
    for result in sqlresults:
        pages[pagesindex].append(result)

        if len(pages[pagesindex]) == 20:
            pages.append([])
            pagesindex += 1

    if len(pages[-1]) == 0:
        del pages[-1]
        pagesindex -= 1

    global currentpage
    currentpage = 0
    global pagecount
    pagecount = pagesindex + 1

    def printpage():
        global currentpage
        global pagecount
        column_widths = getlongest(pages[currentpage])
        clear_console()

        while True:
            print(f'SELECT A RECORD FROM {table.upper()} TABLE')
            print(f'Page {currentpage + 1} of {pagecount}')

            if table == 'Users':
                print(
                    f'{"User ID":<{max(column_widths[0], 10)}}{"First Name":<{max(column_widths[1], 13)}}{"Last Name":<{max(column_widths[2], 12)}}{"Phone":<{column_widths[3]}}{"Email":<{column_widths[4]}}{"Hire Date":<{max(column_widths[5], 12)}}{"Manager":<10}{"Active":<9}')
                for result in pages[currentpage]:
                    print(f'{result[0]:<{max(column_widths[0], 10)}}{result[1]:<{max(column_widths[1], 13)}}{result[2]:<{max(column_widths[2], 12)}}{result[3]:<{column_widths[3]}}{result[4]:<{column_widths[4]}}{result[5]:<{max(column_widths[5], 12)}}{result[6]:<10}{result[7]:<9}')
            elif table == 'Competencies':
                print(
                    f'{"Competency ID":<{max(column_widths[0], 16)}}{"Name":<{column_widths[1]}}{"Date Created":<{max(column_widths[2], 15)}}{"Active":<9}')
                for result in pages[currentpage]:
                    print(
                        f'{result[0]:<{max(column_widths[0], 16)}}{result[1]:<{column_widths[1]}} {result[2]:<{max(column_widths[2], 15)}} {result[3]:<9}')
            elif table == 'Assessments':
                print(
                    f'{"Assessment ID":<{max(column_widths[0], 16)}}{"Competency":<{max(column_widths[1], 13)}}{"Name":<{column_widths[2]}}{"Date Created":<{max(column_widths[3], 15)}}{"Active":<9}')
                for result in pages[currentpage]:
                    print(
                        f'{result[0]:<{max(column_widths[0], 16)}}{result[1]:<{column_widths[1]}}{result[2]:<{column_widths[2]}}{result[3]:<{max(column_widths[3], 15)}}{result[4]:<9}')
            elif table == 'Results':
                print(
                    f'{"Result ID":<{max(column_widths[0], 12)}}{"Assessment":<{column_widths[1]}}{"User":<{column_widths[2]}}{"Score":<8}{"Date Taken":<{max(column_widths[3], 13)}}{"Active":<9}')
                for result in pages[currentpage]:
                    print(
                        f'{result[0]:<{max(column_widths[0], 12)}}{result[1]:<{column_widths[1]}}{result[2]:<{column_widths[2]}}{result[3]:<{max(column_widths[3], 13)}}{result[4]:<9}')

            selection = input(
                f'\n{"Enter N for next page, P for previous, or a page number, enter X to exit." if pagecount > 1 else "Enter X to exit."} {"To select a user, enter # then the user ID. (Example #29):" if table == "Users" else "To select a record, enter # then the ID. (Example #29):"} ')
            if selection.upper() in ['N', 'P', *[str(num) for num in range(1, len(pages) + 1)]]:
                if selection.upper() == 'N' and currentpage + 1 < len(pages):
                    currentpage += 1
                    printpage()
                elif selection.upper() == 'P' and currentpage + 1 > 1:
                    currentpage -= 1
                    printpage()
                elif selection.isdigit() and int(selection) in range(1, len(pages)):
                    currentpage = int(selection) - 1
                    printpage()
                else:
                    printpage()
            elif selection.upper() == 'X':
                break
            elif fullmatch(r'#\d+', selection):
                return int(resplit(r'#', selection, 1)[1])

    lookupcheck = printpage()
    if isinstance(lookupcheck, int):
        return lookupcheck
