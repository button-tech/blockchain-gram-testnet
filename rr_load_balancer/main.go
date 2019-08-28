package main

import (
	"log"
	"net/url"
	"os"
	"sync"
	"time"

	"github.com/anvie/port-scanner"
	"github.com/gin-gonic/gin"
	"github.com/hlts2/round-robin"
	"github.com/imroc/req"
)

type TonTestnet struct {
	sync.RWMutex
	Status bool
	Time   string
}

func (t *TonTestnet) Set(status bool, time string) {
	t.Lock()
	t.Status = status
	t.Time = time
	t.Unlock()
}

func (t *TonTestnet) Get() (bool, string) {
	t.RLock()
	defer t.RUnlock()
	return t.Status, t.Time
}

var (
	T          TonTestnet
	jsonHeader = req.Header{
		"Content-Type": "application/json",
	}
)

func UrlGen(network, request, host, address string) string {

	if len(network) == 0 {
		return host + "/" + request + "/" + address
	}

	return host + "/" + request + "/" + address + "?network=" + network
}

func tonTestnetChecker(ip string, port int) {

	ps := portscanner.NewPortScanner(ip, 1*time.Second, 1)

	log.Println("Start healthCheck!")

	for {

		isAlive := ps.IsOpen(port)

		dt := time.Now()

		if !isAlive {

			time.Sleep(time.Second * 10)

			secondCheck := ps.IsOpen(port)

			dt = time.Now()

			T.Set(secondCheck, dt.Format("01-02-2006T15:04:05"))

			log.Println("TON off!")

			time.Sleep(time.Minute * 1)

			continue
		}

		T.Set(isAlive, dt.Format("01-02-2006T15:04:05"))

		time.Sleep(1 * time.Minute)
	}
}

func init() {
	go tonTestnetChecker("67.207.74.182", 4924)
}

func main() {

	r := gin.New()

	rr, err := roundrobin.New([]*url.URL{
		// Add addresses
	})
	if err != nil {
		log.Println(err)
		os.Exit(1)
	}

	r.GET("/getBalance/:address", func(c *gin.Context) {

		host := rr.Next()

		resp, err := req.Get(UrlGen(c.Request.URL.Query().Get("network"), "getBalance", host.Host, c.Param("address")))
		if err != nil {
			c.JSON(500, err.Error())
			return
		}

		c.Data(resp.Response().StatusCode, "application/json", resp.Bytes())
	})

	r.GET("/getAccount/:catalog", func(c *gin.Context) {

		host := rr.Next()

		resp, err := req.Get(UrlGen(c.Request.URL.Query().Get("network"), "getAccount", host.Host, c.Param("catalog")))
		if err != nil {
			c.JSON(500, err.Error())
			return
		}

		c.Data(resp.Response().StatusCode, "application/json", resp.Bytes())
	})

	r.GET("/healthCheck", func(c *gin.Context) {

		lastTimeCheck, status := T.Get()

		data := struct {
			Up            bool   `json:"up"`
			LastTimeCheck string `json:"lastTimeCheck"`
		}{lastTimeCheck, status}

		c.JSON(200, data)

	})

	r.GET("/getPublicKeyFile/:catalog", func(c *gin.Context) {

		host := rr.Next()

		resp, err := req.Get(UrlGen(c.Request.URL.Query().Get("network"), "getPublicKeyFile", host.Host, c.Param("catalog")))
		if err != nil {
			c.JSON(500, err.Error())
			return
		}

		c.Data(resp.Response().StatusCode, "application/octet-stream", resp.Bytes())
	})

	r.GET("/getPrivateKeyFile/:catalog", func(c *gin.Context) {

		host := rr.Next()

		resp, err := req.Get(UrlGen(c.Request.URL.Query().Get("network"), "getPrivateKeyFile", host.Host, c.Param("catalog")))
		if err != nil {
			c.JSON(500, err.Error())
			return
		}

		c.Data(resp.Response().StatusCode, "application/octet-stream", resp.Bytes())
	})

	r.GET("/getLastTxHash/:address", func(c *gin.Context) {

		host := rr.Next()

		resp, err := req.Get(UrlGen(c.Request.URL.Query().Get("network"), "getLastTxHash", host.Host, c.Param("address")))
		if err != nil {
			c.JSON(500, err.Error())
			return
		}

		c.Data(resp.Response().StatusCode, "application/json", resp.Bytes())
	})

	r.POST("/generateAccount", func(c *gin.Context) {

		host := rr.Next()

		resp, err := req.Post(host.Host+"/generateAccount", jsonHeader, c.Request.Body)
		if err != nil {
			c.JSON(500, err.Error())
			return
		}

		c.Data(resp.Response().StatusCode, "application/json", resp.Bytes())
	})

	r.POST("/send", func(c *gin.Context) {

		host := rr.Next()

		resp, err := req.Post(host.Host+"/send", jsonHeader, c.Request.Body)
		if err != nil {
			c.JSON(500, err.Error())
			return
		}

		c.Data(resp.Response().StatusCode, "application/json", resp.Bytes())
	})

	if err := r.Run(":80"); err != nil {
		log.Println(err)
		os.Exit(1)
	}
}
