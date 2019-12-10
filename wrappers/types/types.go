package types

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
