package basic

import "testing"

func TestRange(t *testing.T) {
	var m = map[string]string{
		"a":"1",
		"b":"2",
	}

	for item := range m {
		println(item)
	}

}
