package handlers

import (
	"encoding/json"
	t "github.com/button-tech/gram-testnet/wrappers/types"
	"github.com/gin-gonic/gin"
	"github.com/imroc/req"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

var (
	// workdir in docker container
	workdir = os.Getenv("WORKDIR")
	header  = req.Header{
		"Content-Type": "application/json",
	}
)

func GetPublicKeyFile(c *gin.Context) {

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
}

func GetPrivateKeyFile(c *gin.Context) {

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
}

func GetAccount(c *gin.Context) {

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

	var result t.Account

	err = json.Unmarshal(byteValue, &result)
	if err != nil {
		c.JSON(500, gin.H{"error": err.Error()})
		return
	}

	c.JSON(200, result)

}

func GetBalance(c *gin.Context) {

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
}

func GenerateAccountWithHook(c *gin.Context) {
	var p t.GeneratedAccount

	err := c.BindJSON(&p)
	if err != nil {
		c.JSON(500, err)
		return
	}

	go generateAccount(p)

	c.JSON(200, "ok")
}

func GenerateAccountSync(c *gin.Context) {
	var p t.GeneratedAccount

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
}

func GetLastTxHash(c *gin.Context) {

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
}

func RegAccount(c *gin.Context) {
	var p t.GeneratedAccount

	err := c.BindJSON(&p)
	if err != nil {
		c.JSON(500, err)
		return
	}

	cmd := exec.Command(workdir+"/reg_account.py", p.CatalogId, p.NetworkId)
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

}

func CheckSeqno(c *gin.Context) {
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
}

func GenerateAccountWithFaucet(c *gin.Context) {
	var p t.GeneratedAccount

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
}

func SendGramsWithHook(c *gin.Context) {
	var p t.TxParams

	err := c.BindJSON(&p)
	if err != nil {
		c.JSON(500, err)
		return
	}

	go sendGrams(p)

	c.JSON(200, gin.H{"success": true})

}

func SendGramsSync(c *gin.Context) {
	var p t.TxParams

	err := c.BindJSON(&p)
	if err != nil {
		c.JSON(500, err)
		return
	}

	if len(p.Network) == 0 {
		p.Network = "-1"
	}

	cmd := exec.Command(workdir+"/send_grams.py", p.SenderId, p.SenderPub, p.RecipientPub, p.Amount, p.Network)
	stdout, err := cmd.Output()
	if err != nil {
		c.JSON(500, err.Error())
		return
	}

	if string(stdout) == "error\n" {
		c.JSON(500, err.Error())
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
		c.JSON(500, err.Error())
		return
	}

	p.SenderTxHash = txResult.SenderTxHash
	p.RecipientTxHash = txResult.RecipientTxHash
	p.Success = true

	c.JSON(200, p)
}

func generateAccount(p t.GeneratedAccount) {

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

func sGenerate(p t.GeneratedAccount, script string) (*t.GeneratedAccount, error) {
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

func sendGrams(p t.TxParams) {

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
