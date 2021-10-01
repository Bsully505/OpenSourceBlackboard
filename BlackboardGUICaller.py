import tkinter as tk
import requests


class mainApp(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.title("Test GUI")

        self.label = tk.Label(parent, text="This is a test GUI")
        self.label.pack()

        self.hello_button = tk.Button(parent, text="PrintHelloWorld", command=self.helloTest)
        self.hello_button.pack()

        self.printButton = tk.Button(parent, text = "Print Text Input", command =self.printResponseForCourseInfo)
        self.printButton.pack()

        self.close_button = tk.Button(parent, text="Close", command=parent.quit)
        self.close_button.pack()

    def helloTest(self):
        print("Hello World!")

    def printResponseForCourseInfo(self):
        #example course id is _90767_1 this is for procedural generation
        input = inputText.get(1.0, "end-1c")
        url = "https://quinnipiac.blackboard.com/learn/api/public/v1/courses/"+input+"/contents"
        response = requests.request("GET",url)
        print(response.json())


if __name__ == "__main__":
    root = tk.Tk()
    inputText = tk.Text(root, height = 2, width = 20)
    inputText.pack()
    label = tk.Label(root, text="Hello World", padx=10, pady=10)
    my_gui =  mainApp(root)
    root.mainloop()


