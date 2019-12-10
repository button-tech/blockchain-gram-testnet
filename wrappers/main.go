package main

import (
	"log"
	"os"

	h "github.com/button-tech/gram-testnet/wrappers/handlers"
	"github.com/gin-gonic/gin"
)

func main() {

	r := gin.New()

	r.Use(gin.Recovery())

	gin.SetMode(gin.ReleaseMode)

	r.GET("/getPublicKeyFile/:catalog", h.GetPublicKeyFile)

	r.GET("/getPrivateKeyFile/:catalog", h.GetPrivateKeyFile)

	r.GET("/getAccount/:catalog", h.GetAccount)

	r.GET("/getBalance/:address", h.GetBalance)

	r.POST("/generateAccount", h.GenerateAccountWithHook)

	r.POST("/sGenerate", h.GenerateAccountSync)

	r.GET("/getLastTxHash/:address", h.GetLastTxHash)

	r.POST("/regAccount", h.RegAccount)

	r.GET("/checkSeqno/:address", h.CheckSeqno)

	r.POST("/sGenerateAndFaucet", h.GenerateAccountWithFaucet)

	r.POST("/send", h.SendGramsWithHook)

	r.POST("/sendGrams", h.SendGramsSync)

	if err := r.Run(":8080"); err != nil {
		log.Println(err)
		os.Exit(1)
	}
}
