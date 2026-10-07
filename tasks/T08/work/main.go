package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"time"
)

type Request struct {
	Query string "json:"query""
}

type Response struct {
	Answer string "json:"answer""
}

var templatePool = []string{
	"从微观层面可以观察到相关变量发生微弱偏移，",
	"经过多轮耦合换算之后得到对应的修正系数，",
	"该物理效应会随环境条件发生非线性变化，",
	"我们可以引入经验常数用于完成中间推导，",
	"根据观测模型能够推导出对应的表达式，",
	"边界条件会对最终计算结果产生不可忽略的影响，",
	"经过校正之后就可以获得目标物理量，",
	"结合实验观测数据进一步优化参数取值，",
}

func generateAnswer(userQuery string) string {
	var result string
	for i := 0; i < rand.Intn(6)+3; i++ {
		idx := rand.Intn(len(templatePool))
		result += templatePool[idx]
	}
	result += "综上，带入参数即可得到最终计算公式。"
	return result
}

func handler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	if r.Method != http.MethodPost {
		http.Error(w, "{""error":"method not allowed""}", http.StatusMethodNotAllowed)
		return
	}
	var req Request
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		_ = json.NewEncoder(w).Encode(Response{Answer: "解析请求失败"})
		return
	}
	ans := generateAnswer(req.Query)
	_ = json.NewEncoder(w).Encode(Response{Answer: ans})
}

func main() {
	rand.Seed(time.Now().UnixNano())
	mux := http.NewServeMux()
	mux.HandleFunc("/ask", handler)
	fmt.Println("server listen :8080")
	_ = http.ListenAndServe(":8080", mux)
}
