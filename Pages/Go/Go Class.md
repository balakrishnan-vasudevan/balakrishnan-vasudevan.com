https://www.youtube.com/playlist?list=PLoILbKo9rG3skRCj37Kn5Zj803hhiuRK6

44 lectures - 3/44
## 0

## 1

```
package main  ====> 
import (
		 "fmt" ====> import any package to use
)

func main() {  ===> main function, where the program starts
		fmt.Println("Hello, world") ===> package.function_name
}
```

Go is a modular language, program can be in different files and packages, main function has to be in package main
Run go:
go run .

Go compiles and runs a program
Binaries don't stick around

## 2
Simple example + Unit tests
```
package main

import (
	"fmt"
	"os"
)

func main() {
		fmt.Println("hello, %s\n", os.Args[1])
}
```

os.Args[0] = name of the program