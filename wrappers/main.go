package main

import (
	"encoding/json"
	"io/ioutil"
	"os"
	"os/exec"
	"strings"

	"io"
	"log"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"

	"github.com/imroc/req"
)

type TxParams struct {
	SenderId        string `json:"senderId"`
	SenderPub       string `json:"senderPub"`
	RecipientPub    string `json:"recipientPub"`
	Amount          string `json:"amount"`
	Network         string `json:"network"`
	Success         bool   `json:"success"`
	FromNick        string `json:"fromNick"`
	ToNick          string `json:"toNick"`
	FromChatId      int64  `json:"fromChatId"`
	ToChatId        int64  `json:"toChatId"`
	SenderTxHash    string `json:"senderTxHash"`
	RecipientTxHash string `json:"recipientTxHash"`
	CompanyGuid     string `json:"companyGuid"`
	CompanyId       string `json:"companyId"`
	WebHookUrl      string `json:"webHookUrl"`
}

type Account struct {
	PublicKeyF string `json:"publicKeyF"`
	PublicKeyS string `json:"publicKeyS"`
	ForInit    string `json:"forInit"`
}

type GeneratedAccount struct {
	PublicKeyF string `json:"publicKeyF"`
	PublicKeyS string `json:"publicKeyS"`
	ForInit    string `json:"forInit"`
	CatalogId  string `json:"catalogId"`
	UserId     int64  `json:"userId"`
	Chain      string `json:"chain"`
	Success    bool   `json:"success,omitempty"`
	NetworkId  string `json:"networkId"`
	WebHookUrl string `json:"webHookUrl,omitempty"`
}

var (
	workdir = os.Getenv("WORKDIR")
	header  = req.Header{
		"Content-Type": "application/json",
	}
)

func generateAccount(p GeneratedAccount) {

	cmd := exec.Command(workdir+"/addr_gen.py", p.NetworkId)

	stdout, err := cmd.Output()
	if err != nil {
		p.Success = false
		jsonValue, _ := json.Marshal(p)
		req.Post(p.WebHookUrl, header, jsonValue)
		return
	}

	if string(stdout) == "error\n" {
		p.Success = false
		jsonValue, _ := json.Marshal(p)
		req.Post(p.WebHookUrl, header, jsonValue)
		return
	}

	results := strings.TrimSuffix(string(stdout), "\n")
	results = strings.Replace(results, "'", "\"", -1)

	err = json.Unmarshal([]byte(results), &p)
	if err != nil {
		p.Success = false
		jsonValue, _ := json.Marshal(p)
		req.Post(p.WebHookUrl, header, jsonValue)
		return
	}

	p.Success = true

	switch p.NetworkId {
	case "0":
		p.Chain = "base"
	case "-1":
		p.Chain = "master"
	}

	jsonValue, _ := json.Marshal(p)

	req.Post(p.WebHookUrl, header, jsonValue)
}

func sGenerate(p GeneratedAccount, script string) (*GeneratedAccount, error) {
	cmd := exec.Command(workdir+"/"+script, p.NetworkId)

	stdout, err := cmd.Output()
	if err != nil {
		return nil, err
	}

	if string(stdout) == "error\n" {
		return nil, err
	}

	results := strings.TrimSuffix(string(stdout), "\n")
	results = strings.Replace(results, "'", "\"", -1)

	err = json.Unmarshal([]byte(results), &p)
	if err != nil {
		return nil, err
	}

	p.Success = true

	switch p.NetworkId {
	case "0":
		p.Chain = "base"
	case "-1":
		p.Chain = "master"
	}

	return &p, nil
}

func sendGrams(p TxParams) {

	if len(p.Network) == 0 {
		p.Network = "-1"
	}

	cmd := exec.Command(workdir+"/send_grams.py", p.SenderId, p.SenderPub, p.RecipientPub, p.Amount, p.Network)
	stdout, err := cmd.Output()
	if err != nil {
		p.Success = false
		jsonValue, _ := json.Marshal(p)
		req.Post(p.WebHookUrl, header, jsonValue)
		return
	}

	if string(stdout) == "error\n" {
		p.Success = false
		jsonValue, _ := json.Marshal(p)
		req.Post(p.WebHookUrl, header, jsonValue)
		return
	}

	txResult := struct {
		SenderTxHash    string `json:"senderTxHash"`
		RecipientTxHash string `json:"recipientTxHash"`
	}{}

	hash := strings.TrimSuffix(string(stdout), "\n")
	hash = strings.Replace(hash, "'", "\"", -1)

	err = json.Unmarshal([]byte(hash), &txResult)
	if err != nil {
		p.Success = false
		jsonValue, _ := json.Marshal(p)
		req.Post(p.WebHookUrl, header, jsonValue)
		return
	}

	p.SenderTxHash = txResult.SenderTxHash
	p.RecipientTxHash = txResult.RecipientTxHash
	p.Success = true

	jsonValue, _ := json.Marshal(p)
	req.Post(p.WebHookUrl, header, jsonValue)
}

func readJSON(catalog string) ([]byte, error) {

	jsonFile, err := os.Open(catalog + "/pub.json")
	if err != nil {
		return nil, err
	}
	defer jsonFile.Close()

	byteValue, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		return nil, err
	}

	return byteValue, nil
}

func main() {

	r := gin.New()

	r.Use(gin.Recovery())

	gin.SetMode(gin.ReleaseMode)

	r.GET("/getPublicKeyFile/:catalog", func(c *gin.Context) {

		network := c.Request.URL.Query().Get("network")

		if len(network) == 0 {
			network = "masterchain"
		}

		catalog := workdir + "/" + network + "/" + c.Param("catalog")

		filename := c.Param("catalog") + ".addr"

		OpenFile, err := os.Open(catalog + "/" + filename)
		defer OpenFile.Close()
		if err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}

		FileHeader := make([]byte, 512)
		OpenFile.Read(FileHeader)
		FileContentType := http.DetectContentType(FileHeader)
		FileStat, _ := OpenFile.Stat()
		FileSize := strconv.FormatInt(FileStat.Size(), 10)

		c.Header("Content-Type", FileContentType)
		c.Header("Content-Disposition", "attachment; filename="+filename)
		c.Header("Content-Length", FileSize)

		OpenFile.Seek(0, 0)

		io.Copy(c.Writer, OpenFile)
	})

	r.GET("/getPrivateKeyFile/:catalog", func(c *gin.Context) {

		network := c.Request.URL.Query().Get("network")

		if len(network) == 0 {
			network = "masterchain"
		}

		catalog := workdir + "/" + network + "/" + c.Param("catalog")

		filename := c.Param("catalog") + ".pk"

		OpenFile, err := os.Open(catalog + "/" + filename)
		defer OpenFile.Close()
		if err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}

		FileHeader := make([]byte, 512)
		OpenFile.Read(FileHeader)
		FileContentType := http.DetectContentType(FileHeader)
		FileStat, _ := OpenFile.Stat()
		FileSize := strconv.FormatInt(FileStat.Size(), 10)

		c.Header("Content-Type", FileContentType)
		c.Header("Content-Disposition", "attachment; filename="+filename)
		c.Header("Content-Length", FileSize)

		OpenFile.Seek(0, 0)

		io.Copy(c.Writer, OpenFile)
	})

	r.GET("/getAccount/:catalog", func(c *gin.Context) {

		network := c.Request.URL.Query().Get("network")

		if len(network) == 0 {
			network = "masterchain"
		}

		catalog := workdir + "/" + network + "/" + c.Param("catalog")

		byteValue, err := readJSON(catalog)
		if err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}

		var result Account

		err = json.Unmarshal(byteValue, &result)
		if err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			return
		}

		c.JSON(200, result)

	})

	r.GET("/getBalance/:address", func(c *gin.Context) {

		network := c.Request.URL.Query().Get("network")

		if network == "masterchain" {
			network = "-1"
		} else if network == "basechain" {
			network = "0"
		} else if len(network) == 0 {
			network = "-1"
		}

		cmd := exec.Command(workdir+"/get_balance.py", c.Param("address"), network)
		stdout, err := cmd.Output()
		if err != nil {
			c.JSON(500, err.Error())
			return
		}
		if string(stdout) == "error\n" {
			c.JSON(500, gin.H{"error": "Can't get balance"})
			return
		}

		balance := strings.TrimSuffix(string(stdout), "\n")

		c.JSON(200, gin.H{"nanograms": balance})
	})

	r.POST("/generateAccount", func(c *gin.Context) {
		var p GeneratedAccount

		err := c.BindJSON(&p)
		if err != nil {
			c.JSON(500, err)
			return
		}

		go generateAccount(p)

		c.JSON(200, "ok")
	})

	r.POST("/sGenerate", func(c *gin.Context) {
		var p GeneratedAccount

		err := c.BindJSON(&p)
		if err != nil {
			c.JSON(500, err)
			return
		}

		result, err := sGenerate(p, "addr_gen.py")
		if err != nil {
			c.JSON(500, err)
			return
		}

		c.JSON(200, result)
	})

	r.GET("/getLastTxHash/:address", func(c *gin.Context) {

		network := c.Request.URL.Query().Get("network")

		if network == "masterchain" {
			network = "-1"
		} else if network == "basechain" {
			network = "0"
		} else if len(network) == 0 {
			network = "-1"
		}

		cmd := exec.Command(workdir+"/get_last_tx_hash.py", c.Param("address"), network)
		stdout, err := cmd.Output()
		if err != nil {
			c.JSON(500, err.Error())
			return
		}
		if string(stdout) == "error\n" {
			c.JSON(500, gin.H{"error": "Can't get balance"})
			return
		}

		hash := strings.TrimSuffix(string(stdout), "\n")

		c.JSON(200, gin.H{"txHash": hash})
	})

	r.GET("/regAccount/:catalog", func(c *gin.Context) {
		network := c.Request.URL.Query().Get("network")

		if network == "masterchain" {
			network = "-1"
		} else if network == "basechain" {
			network = "0"
		} else if len(network) == 0 {
			network = "-1"
		}

		cmd := exec.Command(workdir+"/reg_account.py", c.Param("catalog"), network)
		stdout, err := cmd.Output()
		if err != nil {
			c.JSON(500, err.Error())
			return
		}
		if string(stdout) == "False\n" {
			c.JSON(500, gin.H{"reg": "error"})
			return
		} else if string(stdout) == "True\n" {
			c.JSON(200, gin.H{"reg": "nice"})
			return
		}

	})

	r.GET("/checkSeqno/:address", func(c *gin.Context) {
		network := c.Request.URL.Query().Get("network")

		if network == "masterchain" {
			network = "-1"
		} else if network == "basechain" {
			network = "0"
		} else if len(network) == 0 {
			network = "-1"
		}

		cmd := exec.Command(workdir+"/check_seqno.py", c.Param("address"), network)
		stdout, err := cmd.Output()
		if err != nil {
			c.JSON(500, err.Error())
			return
		}
		if string(stdout) == "False\n" {
			c.JSON(500, gin.H{"ready": "no"})
			return
		} else if string(stdout) == "True\n" {
			c.JSON(200, gin.H{"ready": "yes"})
			return
		}
	})

	r.POST("/sGenerateAndFaucet", func(c *gin.Context) {
		var p GeneratedAccount

		err := c.BindJSON(&p)
		if err != nil {
			c.JSON(500, err)
			return
		}

		result, err := sGenerate(p, "gen_and_faucet.py")
		if err != nil {
			c.JSON(500, err)
			return
		}

		c.JSON(200, result)
	})

	r.POST("/send", func(c *gin.Context) {
		var p TxParams

		err := c.BindJSON(&p)
		if err != nil {
			c.JSON(500, err)
			return
		}

		go sendGrams(p)

		c.JSON(200, gin.H{"success": true})

	})

	if err := r.Run(":80"); err != nil {
		log.Println(err)
		os.Exit(1)
	}
}
